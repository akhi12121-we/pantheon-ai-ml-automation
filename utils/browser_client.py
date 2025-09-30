#!/usr/bin/env python3
"""
Playwright browser client for UI automation.
"""
import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from config.settings import config
from utils.logger import logger

class BrowserClient:
    """Playwright browser client for UI automation."""
    
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        
    async def start_browser(self, browser_type: str = None, headless: bool = None, args: list = None):
        """Start browser instance with enhanced configuration."""
        browser_type = browser_type or config.BROWSER_TYPE
        headless = headless if headless is not None else config.get_headless_mode()
        
        logger.info(f"Starting {browser_type} browser (headless: {headless}, mode: {config.HEADLESS_MODE})")
        
        self.playwright = await async_playwright().start()
        
        # Get browser launcher
        if browser_type == "chromium":
            browser_launcher = self.playwright.chromium
        elif browser_type == "firefox":
            browser_launcher = self.playwright.firefox
        elif browser_type == "webkit":
            browser_launcher = self.playwright.webkit
        else:
            raise ValueError(f"Unsupported browser type: {browser_type}")
        
        # Use simple launch options like recorded script
        launch_options = {
            "headless": headless
        }
        
        # Add custom args if provided
        if args:
            launch_options["args"] = args
        
        self.browser = await browser_launcher.launch(**launch_options)
        
        # Get mobile device config if specified
        mobile_device = config.get_mobile_device_config()
        
        # Create simple context options like recorded script
        context_options = {}
        
        # Add ignore HTTPS errors if args contain certificate flags
        if args and any("certificate" in arg or "ssl" in arg for arg in args):
            context_options["ignore_https_errors"] = True
        
        # Add video recording if enabled for failures
        if config.should_record_video_for_failure():
            context_options["record_video_dir"] = config.VIDEO_PATH
        
        # Add mobile device config if specified
        if mobile_device:
            context_options.update(mobile_device)
        
        # Create context
        self.context = await self.browser.new_context(**context_options)
        
        # Create page
        self.page = await self.context.new_page()
        
        # Set timeouts
        self.page.set_default_timeout(config.DEFAULT_TIMEOUT)
        self.page.set_default_navigation_timeout(config.NAVIGATION_TIMEOUT)
        
        # Set up network monitoring if enabled
        if config.ENABLE_NETWORK_MONITORING:
            await self._setup_network_monitoring()
        
        # Set up performance monitoring if enabled
        if config.ENABLE_PERFORMANCE_MONITORING:
            await self._setup_performance_monitoring()
        
        logger.info("Browser started successfully")
        
    async def close_browser(self):
        """Close browser instance."""
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        
        logger.info("Browser closed")
        
    async def navigate_to(self, url: str):
        """Navigate to URL."""
        logger.info(f"Navigating to: {url}")
        
        # Wait for navigation based on config
        wait_until = config.WAIT_FOR_NAVIGATION
        await self.page.goto(url, wait_until=wait_until)
        
        # Wait for load state
        await self.page.wait_for_load_state(config.WAIT_FOR_LOAD_STATE)
        
    async def click(self, selector: str):
        """Click element with retry logic."""
        logger.info(f"Clicking element: {selector}")
        
        for attempt in range(config.CLICK_RETRY_COUNT):
            try:
                await self.page.click(selector)
                if config.CLICK_DELAY > 0:
                    await asyncio.sleep(config.CLICK_DELAY / 1000)
                return
            except Exception as e:
                if attempt == config.CLICK_RETRY_COUNT - 1:
                    raise e
                await asyncio.sleep(config.UI_RETRY_DELAY)
        
    async def fill(self, selector: str, text: str):
        """Fill input field with retry logic."""
        logger.info(f"Filling field {selector} with: {text[:10]}...")
        
        for attempt in range(config.FILL_RETRY_COUNT):
            try:
                await self.page.fill(selector, text)
                if config.TYPE_DELAY > 0:
                    await asyncio.sleep(config.TYPE_DELAY / 1000)
                return
            except Exception as e:
                if attempt == config.FILL_RETRY_COUNT - 1:
                    raise e
                await asyncio.sleep(config.UI_RETRY_DELAY)
        
    async def get_text(self, selector: str) -> str:
        """Get element text."""
        text = await self.page.text_content(selector)
        logger.info(f"Got text from {selector}: {text[:50]}...")
        return text
        
    async def wait_for_element(self, selector: str, timeout: int = None):
        """Wait for element to be visible."""
        timeout = timeout or config.ELEMENT_TIMEOUT
        logger.info(f"Waiting for element: {selector}")
        
        for attempt in range(config.WAIT_RETRY_COUNT):
            try:
                await self.page.wait_for_selector(selector, timeout=timeout)
                return
            except Exception as e:
                if attempt == config.WAIT_RETRY_COUNT - 1:
                    raise e
                await asyncio.sleep(config.UI_RETRY_DELAY)
        
    async def take_screenshot(self, name: str = None, full_page: bool = None, test_failed: bool = False):
        """Take screenshot with configurable options and failure detection."""
        # Check if screenshots should be taken based on failure status
        if test_failed and not config.should_take_screenshot_for_failure():
            logger.info("Screenshot skipped - not configured for failed tests only")
            return None
        elif not test_failed and config.SCREENSHOT_FAILED_TESTS_ONLY:
            logger.info("Screenshot skipped - only taking screenshots for failed tests")
            return None
        elif not config.should_take_screenshots():
            return None
            
        if not name:
            name = f"screenshot_{int(asyncio.get_event_loop().time())}"
            
        # Use config settings if not specified
        if full_page is None:
            full_page = config.SCREENSHOT_FULL_PAGE
            
        # Create screenshots directory
        screenshot_dir = Path(config.SCREENSHOT_PATH)
        screenshot_dir.mkdir(exist_ok=True)
        
        # Generate filename based on config and failure status
        timestamp = int(asyncio.get_event_loop().time())
        failure_suffix = "_FAILED" if test_failed else "_SUCCESS"
        
        if config.SCREENSHOT_INCLUDE_TEST_NAME and config.SCREENSHOT_INCLUDE_TIMESTAMP:
            filename = f"{name}{failure_suffix}_{timestamp}.{config.SCREENSHOT_FORMAT}"
        elif config.SCREENSHOT_INCLUDE_TEST_NAME:
            filename = f"{name}{failure_suffix}.{config.SCREENSHOT_FORMAT}"
        elif config.SCREENSHOT_INCLUDE_TIMESTAMP:
            filename = f"screenshot{failure_suffix}_{timestamp}.{config.SCREENSHOT_FORMAT}"
        else:
            filename = f"{name}{failure_suffix}.{config.SCREENSHOT_FORMAT}"
        
        screenshot_path = screenshot_dir / filename
        
        # Take screenshot with quality settings for JPEG
        screenshot_options = {
            "path": str(screenshot_path),
            "full_page": full_page
        }
        
        if config.SCREENSHOT_FORMAT == "jpeg":
            screenshot_options["quality"] = config.SCREENSHOT_QUALITY
        
        await self.page.screenshot(**screenshot_options)
        
        status = "FAILED" if test_failed else "SUCCESS"
        logger.info(f"Screenshot saved ({status}): {screenshot_path}")
        return str(screenshot_path)
        
    async def get_page_title(self) -> str:
        """Get page title."""
        title = await self.page.title()
        logger.info(f"Page title: {title}")
        return title
        
    async def get_current_url(self) -> str:
        """Get current URL."""
        url = self.page.url
        logger.info(f"Current URL: {url}")
        return url
        
    async def wait_for_url(self, url_pattern: str, timeout: int = None):
        """Wait for URL to match pattern."""
        timeout = timeout or config.DEFAULT_TIMEOUT
        logger.info(f"Waiting for URL pattern: {url_pattern}")
        await self.page.wait_for_url(url_pattern, timeout=timeout)
        
    async def execute_script(self, script: str):
        """Execute JavaScript."""
        logger.info(f"Executing script: {script[:50]}...")
        result = await self.page.evaluate(script)
        return result
        
    async def mock_api_response(self, url_pattern: str, response_data: dict, status: int = 200):
        """Mock API response."""
        logger.info(f"Mocking API response for: {url_pattern}")
        
        async def handle_route(route):
            await route.fulfill(
                status=status,
                content_type="application/json",
                body=str(response_data).replace("'", '"')
            )
            
        await self.page.route(url_pattern, handle_route)
        
    async def intercept_requests(self, url_pattern: str = None):
        """Intercept and log requests."""
        logger.info(f"Intercepting requests for: {url_pattern or 'all'}")
        
        async def handle_request(request):
            logger.info(f"Request: {request.method} {request.url}")
            
        async def handle_response(response):
            logger.info(f"Response: {response.status} {response.url}")
            
        if url_pattern:
            self.page.on("request", lambda request: handle_request(request) if url_pattern in request.url else None)
            self.page.on("response", lambda response: handle_response(response) if url_pattern in response.url else None)
        else:
            self.page.on("request", handle_request)
            self.page.on("response", handle_response)
    
    async def _setup_network_monitoring(self):
        """Setup network monitoring."""
        logger.info("Setting up network monitoring")
        
        async def handle_request(request):
            if config.LOG_NETWORK_REQUESTS:
                logger.info(f"🌐 Request: {request.method} {request.url}")
        
        async def handle_response(response):
            if config.LOG_NETWORK_REQUESTS:
                logger.info(f"📡 Response: {response.status} {response.url}")
        
        self.page.on("request", handle_request)
        self.page.on("response", handle_response)
    
    async def _setup_performance_monitoring(self):
        """Setup performance monitoring."""
        logger.info("Setting up performance monitoring")
        
        # Enable performance metrics
        await self.page.add_init_script("""
            window.performanceMetrics = {
                loadTime: 0,
                domContentLoaded: 0,
                firstPaint: 0
            };
            
            window.addEventListener('load', () => {
                const perfData = performance.getEntriesByType('navigation')[0];
                window.performanceMetrics.loadTime = perfData.loadEventEnd - perfData.loadEventStart;
                window.performanceMetrics.domContentLoaded = perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart;
                
                const paintEntries = performance.getEntriesByType('paint');
                if (paintEntries.length > 0) {
                    window.performanceMetrics.firstPaint = paintEntries[0].startTime;
                }
            });
        """)
    
    async def get_performance_metrics(self):
        """Get performance metrics."""
        if not config.ENABLE_PERFORMANCE_MONITORING:
            return None
            
        try:
            metrics = await self.page.evaluate("window.performanceMetrics")
            logger.info(f"Performance metrics: {metrics}")
            return metrics
        except Exception as e:
            logger.warning(f"Could not get performance metrics: {e}")
            return None
    
    async def save_video(self, test_name: str = None, test_failed: bool = False):
        """Save video recording with failure detection."""
        # Check if video should be saved based on failure status
        if test_failed and not config.should_record_video_for_failure():
            logger.info("Video recording skipped - not configured for failed tests only")
            return None
        elif not test_failed and config.VIDEO_FAILED_TESTS_ONLY:
            logger.info("Video recording skipped - only recording videos for failed tests")
            return None
        elif not config.should_record_video():
            return None
            
        try:
            video_path = await self.page.video.path()
            if video_path and test_name:
                # Create videos directory
                video_dir = Path(config.VIDEO_PATH)
                video_dir.mkdir(exist_ok=True)
                
                # Generate new filename with failure status
                timestamp = int(asyncio.get_event_loop().time())
                failure_suffix = "_FAILED" if test_failed else "_SUCCESS"
                new_filename = f"{test_name}{failure_suffix}_{timestamp}.{config.VIDEO_FORMAT}"
                new_path = video_dir / new_filename
                
                # Move video file
                import shutil
                shutil.move(video_path, new_path)
                
                status = "FAILED" if test_failed else "SUCCESS"
                logger.info(f"Video saved ({status}): {new_path}")
                return str(new_path)
        except Exception as e:
            logger.warning(f"Could not save video: {e}")
            return None

# Global browser client instance
browser_client = BrowserClient()
