"""
Comprehensive configuration settings for API and UI automation.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Comprehensive configuration class for automation framework."""
    
    # ===========================================
    # API CONFIGURATION
    # ===========================================
    
    # API URLs - All main URLs for different APIs
    AIQE_URL = os.getenv("AIQE_URL", "https://aiqe-api.example.com")
    APIE_URL = os.getenv("APIE_URL", "https://apie-api.example.com")
    FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000")
    APOLLO_URL = os.getenv("APOLLO_URL", "https://apollo.welocalize.io")
    COMET_URL = os.getenv("COMET_URL", "https://comet-api.example.com")
    
    # Additional API URLs (add more as needed)
    WELOCALIZE_URL = os.getenv("WELOCALIZE_URL", "https://apollo.welocalize.io")
    LOCAL_API_URL = os.getenv("LOCAL_API_URL", "http://localhost:3000")
    STAGING_API_URL = os.getenv("STAGING_API_URL", "https://staging-api.example.com")
    PRODUCTION_API_URL = os.getenv("PRODUCTION_API_URL", "https://api.example.com")
    
    # Authentication
    AUTH_TOKEN = os.getenv("AUTH_TOKEN")
    AUTH_TOKEN_PANTHEON = "eyJqd3QiOiJleUpoYkdjaU9pSlNVekkxTmlJc0luUjVjQ0k2SWtwWFZDSXNJbU4wZVNJNklrcFhWQ0lzSW1wcmRTSTZJaUlzSW10cFpDSTZJaUo5LmV5SndZVzUwYUdWdmJrRjFkR2hVZVhCbElqb2lkWE5sY2lJc0ltOXJkR0ZKWkNJNkluWmhkMjkyYjJ3eE1EUkFhSEpoYVdacExtTnZiU0lzSW5CeWFXNWphWEJoYkNJNk56UTNOVGsxTENKaGRXUnBaVzVqWlNJNk1qRTFOellzSW1sdWRHVnlibUZzSWpwMGNuVmxMQ0p2Y21kaGJtbDZZWFJwYjI1SlpDSTZNakUxTnpZc0luSnZiR1Z6SWpwYkltRmtiV2x1SWl3aWRtVnVaRzl5TFcxaGJtRm5aWElpTENKa1pYWmxiRzl3WlhJaVhTd2libUZ0WlNJNklrOXViSGtnTkNCQmRYUnZiV0YwYVc5dUlDMGdSR1YyWld4dmNHVnlJQzBnVm1GM2IzWnZiQ0lzSW5WelpYSnVZVzFsSWpvaVQyNXNlU0EwSUVGMWRHOXRZWFJwYjI0Z0xTQkVaWFpsYkc5d1pYSWdMU0JXWVhkdmRtOXNJaXdpYzNSaGRIVnpJam9pWVdOMGFYWmxJaXdpYUdGelVtOWliM1JwWTB0bGVTSTZabUZzYzJVc0ltbGhkQ0k2TVRjMU9ESTVOekE1TXl3aWJtSm1Jam94TnpVNE1qazNNRGt6TENKbGVIQWlPakUzTmpBNU1qVXdPVE1zSW1semN5STZJblZ1YTI1dmQyNGlMQ0poZFdRaU9pSjFibXR1YjNkdUlpd2lhblJwSWpvaWFuZDBPblZ1WkdWbWFXNWxaQzh4TnpVNE1qazNNRGt6SW4wLlh4aWRKNkhsM2s3ZmV0YVQ2eWtzcTIwb0M0R3R1S0ZnMHUtWFFpZy1SODZBR3E1VDFkbVpqc29yMjRVWjBjbDVMbVBadFdYMzR5cWlwMzF1ZnIwWnQ2YWxXbFJWU2NUdEpDbElfeFozWTduV3BSeEZVOE5WX1VzRnhINVN1M0VsNlV3b0wtZTgyWkpYUy1hbFJ2LS13elFzSlhNZlN2Z0RDWWdZbkJfTUxBZVIzaWE1eTVJQndNSW1nQ0pVM0I0R29yY1ZKaTZaV2szQ2lxLUxodWVER1NZVUhJYW1nVWRWZnpQR2VBNzRUS2ZWdEItMy1qaXg0RVY4N0Q5MXBjTEZOeXZzUE9EVnliSkE0dThHSS1hNnFuSnJKbmFrR0RKclE4MEpvLWhtY1FVd1VoOXcwS3NjT0RSNXY3VVFfMG80c196clc3a0NkbkxSbUFUUmlnZ0UyZyIsImlzQXV0aGVudGljYXRlZCI6dHJ1ZSwiX2V4cGlyZSI6MTc4OTgzMzA5NDA3NSwiX21heEFnZSI6MzE1MzYwMDAwMDB9"
    AUTH_TOKEN_RELAY= "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImN0eSI6IkpXVCIsImprdSI6IiIsImtpZCI6IiJ9.eyJwYW50aGVvbkF1dGhUeXBlIjoidXNlciIsIm9rdGFJZCI6InZhd292b2wxMDRAaHJhaWZpLmNvbSIsInByaW5jaXBhbCI6NzQ3NTk1LCJhdWRpZW5jZSI6MjE1NzYsImludGVybmFsIjp0cnVlLCJvcmdhbml6YXRpb25JZCI6MjE1NzYsInJvbGVzIjpbImFkbWluIiwidmVuZG9yLW1hbmFnZXIiLCJkZXZlbG9wZXIiXSwibmFtZSI6Ik9ubHkgNCBBdXRvbWF0aW9uIC0gRGV2ZWxvcGVyIC0gVmF3b3ZvbCIsInVzZXJuYW1lIjoiT25seSA0IEF1dG9tYXRpb24gLSBEZXZlbG9wZXIgLSBWYXdvdm9sIiwic3RhdHVzIjoiYWN0aXZlIiwiaGFzUm9ib3RpY0tleSI6ZmFsc2UsImlhdCI6MTc1ODI5NzA1OSwibmJmIjoxNzU4Mjk3MDU5LCJleHAiOjE3NjA5MjUwNTksImlzcyI6InVua25vd24iLCJhdWQiOiJ1bmtub3duIiwianRpIjoiand0OnVuZGVmaW5lZC8xNzU4Mjk3MDU5In0.uQHso28McOcB3KzKHm5JWePRSRudCCANhIkU_qKiy7C9_AjzIJwtGnmA25ZdkCfl1ToySkNwldZt-mEnGW5gTMpvR20uryP7fKBhZ6Gp0LB-1rKwP8GT1RouiIw_y4X90YDDQ7SGoc5vw9Z_s3Lu2GmJJ4HRKt5qXo6mVBSX8n7c9a1kayE9R224LdWDI9UXQVv2-JlW_MdPTORYTB4owoV-J6ZlwWTLrePjxKTHMmZdsv8eCn_KwdYUNGEmvLIH7wd9G9cffdpYxiScOVBmJ3NHVYM77cTxMqK9239NFuzK9CyKKvDx23dEBsf_LIu8mV1Vs2OWBFIgo9IaiJbOFQ"
    
    # ==========================================
    # WEB UI  Configuration
    # ==========================================
    
    # XTM Project Manager URL
    XTM_URL = os.getenv("XTM_URL", "https://word-uat.welocalize.com/project-manager-gui/login.jsp#!/login")
    
    
    ## Pull Project in Panthon Using UI Developer Tools
    PULL_PROJECT_URL = os.getenv("PULL_PROJECT_URL", "https://junction.welocalize.xyz/developer-admin/jobs/platform-get-projects/completed")
   
    #Pull project API URL Pantheon:
    PULL_PROJECT_API_URL = os.getenv("PULL_PROJECT_API_URL", "https://atreus.welocalize.xyz")
    
    ##Search Pulled Project in Relay
    SEARCH_PULLED_PROJECT_URL = os.getenv("SEARCH_PULLED_PROJECT_URL", "https://relay.welocalize.xyz/")
    
    
    
    
    # ===========================================
    # DATA CONFIGURATION
    # ===========================================
    
    # Data Paths
    DATA_ROOT = os.getenv("DATA_ROOT", "data")
    API_DATA_PATH = os.path.join(DATA_ROOT, "api")
    UI_DATA_PATH = os.path.join(DATA_ROOT, "ui")
    
    # API Data Paths
    API_REQUESTS_PATH = os.path.join(API_DATA_PATH, "requests")
    API_RESPONSES_PATH = os.path.join(API_DATA_PATH, "responses")
    API_SCHEMAS_PATH = os.path.join(API_DATA_PATH, "schemas")
    
    # UI Data Paths
    UI_PAGES_PATH = os.path.join(UI_DATA_PATH, "pages")
    UI_ELEMENTS_PATH = os.path.join(UI_DATA_PATH, "elements")
    UI_TESTDATA_PATH = os.path.join(UI_DATA_PATH, "testdata")
    
    # ===========================================
    # UI AUTOMATION CONFIGURATION
    # ===========================================
    
    # Browser Configuration
    BROWSER_TYPE = os.getenv("BROWSER_TYPE", "chromium")  # chromium, firefox, webkit
    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
    # VIEWPORT_WIDTH = int(os.getenv("VIEWPORT_WIDTH", "1920"))
    # VIEWPORT_HEIGHT = int(os.getenv("VIEWPORT_HEIGHT", "1080"))
    
    # Enhanced Headless Mode Control
    HEADLESS_MODE = os.getenv("HEADLESS_MODE", "true").lower()  # auto, true, false, debug
    HEADLESS_DEBUG = os.getenv("HEADLESS_DEBUG", "false").lower() == "false"  # Show browser in debug mode
    HEADLESS_SLOW_MO = int(os.getenv("HEADLESS_SLOW_MO", "0"))  # Slow down operations (ms)
    
    # Simple Headless Control (Easy True/False)
    RUN_HEADLESS = os.getenv("RUN_HEADLESS", "true").lower() == "true"  # Simple true/false control
    
    # Base URLs for UI Testing
    BASE_URL = os.getenv("BASE_URL", "https://apollo.welocalize.io")
    LOGIN_URL = os.getenv("LOGIN_URL", f"{BASE_URL}/login")
    DASHBOARD_URL = os.getenv("DASHBOARD_URL", f"{BASE_URL}/dashboard")
    PatheonURL = os.getenv("PatheonURL", "https://relay.welocalize.xyz/")
    
    
    # ===========================================
    # TIMEOUT CONFIGURATION
    # ===========================================
    
    # API Timeouts
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))  # seconds
    API_CONNECT_TIMEOUT = int(os.getenv("API_CONNECT_TIMEOUT", "10"))  # seconds
    API_READ_TIMEOUT = int(os.getenv("API_READ_TIMEOUT", "30"))  # seconds
    
    # UI Timeouts (in milliseconds)
    DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "30000"))  # 30 seconds
    NAVIGATION_TIMEOUT = int(os.getenv("NAVIGATION_TIMEOUT", "60000"))  # 60 seconds
    ELEMENT_TIMEOUT = int(os.getenv("ELEMENT_TIMEOUT", "30000"))  # 30 seconds
    PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "30000"))  # 30 seconds
    NETWORK_IDLE_TIMEOUT = int(os.getenv("NETWORK_IDLE_TIMEOUT", "5000"))  # 5 seconds
    
    # ===========================================
    # RETRY CONFIGURATION
    # ===========================================
    
    # API Retries
    API_RETRY_COUNT = int(os.getenv("API_RETRY_COUNT", "3"))
    API_RETRY_DELAY = float(os.getenv("API_RETRY_DELAY", "1.0"))  # seconds
    API_RETRY_BACKOFF = float(os.getenv("API_RETRY_BACKOFF", "2.0"))  # multiplier
    
    # UI Retries
    UI_RETRY_COUNT = int(os.getenv("UI_RETRY_COUNT", "3"))
    UI_RETRY_DELAY = float(os.getenv("UI_RETRY_DELAY", "1.0"))  # seconds
    UI_RETRY_BACKOFF = float(os.getenv("UI_RETRY_BACKOFF", "1.5"))  # multiplier
    
    # Element Interaction Retries
    CLICK_RETRY_COUNT = int(os.getenv("CLICK_RETRY_COUNT", "3"))
    FILL_RETRY_COUNT = int(os.getenv("FILL_RETRY_COUNT", "3"))
    WAIT_RETRY_COUNT = int(os.getenv("WAIT_RETRY_COUNT", "5"))
    
    # ===========================================
    # SCREENSHOT CONFIGURATION
    # ===========================================
    
    # Screenshot Settings - Optimized for Failed Tests Only
    SCREENSHOT_ON_FAILURE = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"
    SCREENSHOT_ON_SUCCESS = os.getenv("SCREENSHOT_ON_SUCCESS", "false").lower() == "true"
    SCREENSHOT_FULL_PAGE = os.getenv("SCREENSHOT_FULL_PAGE", "true").lower() == "true"
    SCREENSHOT_PATH = os.getenv("SCREENSHOT_PATH", "screenshots")
    SCREENSHOT_FORMAT = os.getenv("SCREENSHOT_FORMAT", "png")  # png, jpeg
    SCREENSHOT_QUALITY = int(os.getenv("SCREENSHOT_QUALITY", "90"))  # 1-100 for jpeg
    
    # Screenshot Naming
    SCREENSHOT_NAMING = os.getenv("SCREENSHOT_NAMING", "timestamp")  # timestamp, test_name, both
    SCREENSHOT_INCLUDE_TEST_NAME = os.getenv("SCREENSHOT_INCLUDE_TEST_NAME", "true").lower() == "true"
    SCREENSHOT_INCLUDE_TIMESTAMP = os.getenv("SCREENSHOT_INCLUDE_TIMESTAMP", "true").lower() == "true"
    
    # Screenshot Failure Details
    SCREENSHOT_INCLUDE_ERROR_MESSAGE = os.getenv("SCREENSHOT_INCLUDE_ERROR_MESSAGE", "true").lower() == "true"
    SCREENSHOT_FAILED_TESTS_ONLY = os.getenv("SCREENSHOT_FAILED_TESTS_ONLY", "true").lower() == "true"
    
    # ===========================================
    # VIDEO RECORDING CONFIGURATION
    # ===========================================
    
    # Video Recording Settings - Playwright handles failure-only automatically
    VIDEO_RECORDING = os.getenv("VIDEO_RECORDING", "true").lower() == "false"
    VIDEO_PATH = os.getenv("VIDEO_PATH", "videos")
    VIDEO_FORMAT = os.getenv("VIDEO_FORMAT", "webm")  # webm, mp4
    VIDEO_QUALITY = os.getenv("VIDEO_QUALITY", "medium")  # low, medium, high
    
    # Video Recording Options
    VIDEO_SIZE = os.getenv("VIDEO_SIZE", "1280x720")  # width x height
    VIDEO_FPS = int(os.getenv("VIDEO_FPS", "25"))  # frames per second
    VIDEO_BITRATE = os.getenv("VIDEO_BITRATE", "1000k")  # bitrate
    
    # Video Failure Details
    VIDEO_FAILED_TESTS_ONLY = os.getenv("VIDEO_FAILED_TESTS_ONLY", "true").lower() == "true"
    VIDEO_INCLUDE_ERROR_MESSAGE = os.getenv("VIDEO_INCLUDE_ERROR_MESSAGE", "true").lower() == "true"
    
    # ===========================================
    # NAVIGATION CONFIGURATION
    # ===========================================
    
    # Navigation Settings
    WAIT_FOR_NAVIGATION = os.getenv("WAIT_FOR_NAVIGATION", "networkidle").lower()  # load, domcontentloaded, networkidle
    WAIT_FOR_LOAD_STATE = os.getenv("WAIT_FOR_LOAD_STATE", "networkidle").lower()  # load, domcontentloaded, networkidle
    IGNORE_HTTPS_ERRORS = os.getenv("IGNORE_HTTPS_ERRORS", "false").lower() == "true"
    ACCEPT_DOWNLOADS = os.getenv("ACCEPT_DOWNLOADS", "true").lower() == "true"
    
    # Page Load Strategy
    PAGE_LOAD_STRATEGY = os.getenv("PAGE_LOAD_STRATEGY", "normal")  # normal, eager, none
    BLOCK_RESOURCES = os.getenv("BLOCK_RESOURCES", "false").lower() == "true"
    BLOCKED_RESOURCES = os.getenv("BLOCKED_RESOURCES", "image,media,font").split(",")
    
    # ===========================================
    # LOCATOR CONFIGURATION
    # ===========================================
    
    # Locator Strategy
    DEFAULT_LOCATOR_STRATEGY = os.getenv("DEFAULT_LOCATOR_STRATEGY", "css")  # css, xpath, text, role
    LOCATOR_TIMEOUT = int(os.getenv("LOCATOR_TIMEOUT", "30000"))  # milliseconds
    LOCATOR_RETRY_COUNT = int(os.getenv("LOCATOR_RETRY_COUNT", "3"))
    
    # Element Interaction
    CLICK_DELAY = int(os.getenv("CLICK_DELAY", "0"))  # milliseconds
    TYPE_DELAY = int(os.getenv("TYPE_DELAY", "0"))  # milliseconds
    HOVER_DELAY = int(os.getenv("HOVER_DELAY", "0"))  # milliseconds
    
    # ===========================================
    # PERFORMANCE CONFIGURATION
    # ===========================================
    
    # Performance Monitoring
    ENABLE_PERFORMANCE_MONITORING = os.getenv("ENABLE_PERFORMANCE_MONITORING", "false").lower() == "true"
    PERFORMANCE_THRESHOLD = int(os.getenv("PERFORMANCE_THRESHOLD", "5000"))  # milliseconds
    TRACK_METRICS = os.getenv("TRACK_METRICS", "load_time,dom_content_loaded,first_paint").split(",")
    
    # Network Monitoring
    ENABLE_NETWORK_MONITORING = os.getenv("ENABLE_NETWORK_MONITORING", "false").lower() == "true"
    LOG_NETWORK_REQUESTS = os.getenv("LOG_NETWORK_REQUESTS", "false").lower() == "true"
    BLOCK_NETWORK_REQUESTS = os.getenv("BLOCK_NETWORK_REQUESTS", "false").lower() == "true"
    
    # ===========================================
    # BROWSER ARGUMENTS
    # ===========================================
    
    # Browser Arguments
    BROWSER_ARGS = [
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-gpu",
        "--disable-web-security",
        "--allow-running-insecure-content",
        "--disable-extensions",
        "--disable-plugins",
        "--disable-dev-tools",
        "--disable-images" if os.getenv("DISABLE_IMAGES", "false").lower() == "true" else "",
        "--disable-javascript" if os.getenv("DISABLE_JAVASCRIPT", "false").lower() == "true" else "",
    ]
    
    # Remove empty strings
    BROWSER_ARGS = [arg for arg in BROWSER_ARGS if arg]
    
    # ===========================================
    # MOBILE DEVICE EMULATION
    # ===========================================
    
    # Mobile Device Settings
    MOBILE_DEVICE = os.getenv("MOBILE_DEVICE", "none")  # none, iPhone_12, Samsung_Galaxy_S21
    MOBILE_DEVICES = {
        "iPhone_12": {
            "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X)",
            "viewport": {"width": 390, "height": 844},
            "device_scale_factor": 3,
            "is_mobile": True,
            "has_touch": True
        },
        "Samsung_Galaxy_S21": {
            "user_agent": "Mozilla/5.0 (Linux; Android 11; SM-G991B)",
            "viewport": {"width": 384, "height": 854},
            "device_scale_factor": 3,
            "is_mobile": True,
            "has_touch": True
        },
        "iPad": {
            "user_agent": "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X)",
            "viewport": {"width": 768, "height": 1024},
            "device_scale_factor": 2,
            "is_mobile": True,
            "has_touch": True
        }
    }
    
    # ===========================================
    # TEST EXECUTION CONFIGURATION
    # ===========================================
    
    # Test Settings
    TIMEOUT = int(os.getenv("TIMEOUT", "30"))  # Legacy - use specific timeouts above
    PARALLEL_WORKERS = int(os.getenv("PARALLEL_WORKERS", "2"))
    MAX_FAILURES = int(os.getenv("MAX_FAILURES", "5"))
    
    # Test Data
    TEST_DATA_PATH = os.getenv("TEST_DATA_PATH", "test_data")
    FIXTURES_PATH = os.getenv("FIXTURES_PATH", "fixtures")
    
    # ===========================================
    # REPORTING CONFIGURATION
    # ===========================================
    
    # Reporting Settings
    GENERATE_HTML_REPORT = os.getenv("GENERATE_HTML_REPORT", "true").lower() == "true"
    GENERATE_ALLURE_REPORT = os.getenv("GENERATE_ALLURE_REPORT", "true").lower() == "true"
    GENERATE_COVERAGE_REPORT = os.getenv("GENERATE_COVERAGE_REPORT", "true").lower() == "true"
    REPORT_PATH = os.getenv("REPORT_PATH", "reports")
    
    # Allure Configuration
    ALLURE_RESULTS_PATH = os.getenv("ALLURE_RESULTS_PATH", "allure-results")
    ALLURE_REPORT_PATH = os.getenv("ALLURE_REPORT_PATH", "allure-report")
    ALLURE_ENVIRONMENT = os.getenv("ALLURE_ENVIRONMENT", "test")
    
    # ===========================================
    # LOGGING CONFIGURATION
    # ===========================================
    
    # Logging Settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_PATH = os.getenv("LOG_PATH", "logs")
    LOG_FORMAT = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    LOG_FILE_MAX_SIZE = int(os.getenv("LOG_FILE_MAX_SIZE", "10485760"))  # 10MB
    LOG_BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", "5"))
    
    # ===========================================
    # CI/CD CONFIGURATION
    # ===========================================
    
    # CI/CD Settings
    CI_MODE = os.getenv("CI", "false").lower() == "true"
    GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS", "false").lower() == "true"
    JENKINS = os.getenv("JENKINS", "false").lower() == "true"
    
    # CI/CD Specific Settings
    CI_HEADLESS = os.getenv("CI_HEADLESS", "true").lower() == "true"
    CI_SCREENSHOT_ON_FAILURE = os.getenv("CI_SCREENSHOT_ON_FAILURE", "true").lower() == "true"
    CI_VIDEO_RECORDING = os.getenv("CI_VIDEO_RECORDING", "false").lower() == "true"
    
    # ===========================================
    # UTILITY METHODS
    # ===========================================
    
    @classmethod
    def get_mobile_device_config(cls, device_name: str = None):
        """Get mobile device configuration."""
        device_name = device_name or cls.MOBILE_DEVICE
        if device_name == "none":
            return None
        return cls.MOBILE_DEVICES.get(device_name)
    
    @classmethod
    def get_browser_args(cls):
        """Get browser arguments as list."""
        return cls.BROWSER_ARGS.copy()
    
    @classmethod
    def is_ci_mode(cls):
        """Check if running in CI mode."""
        return cls.CI_MODE or cls.GITHUB_ACTIONS or cls.JENKINS
    
    @classmethod
    def should_record_video(cls):
        """Check if video recording should be enabled."""
        if cls.is_ci_mode():
            return cls.CI_VIDEO_RECORDING
        return cls.VIDEO_RECORDING
    
    @classmethod
    def should_take_screenshots(cls):
        """Check if screenshots should be taken."""
        if cls.is_ci_mode():
            return cls.CI_SCREENSHOT_ON_FAILURE
        return cls.SCREENSHOT_ON_FAILURE
    
    @classmethod
    def get_headless_mode(cls):
        """Get headless mode setting with enhanced control."""
        # Simple control - if RUN_HEADLESS is set, use it directly
        if hasattr(cls, 'RUN_HEADLESS') and cls.RUN_HEADLESS is not None:
            return cls.RUN_HEADLESS
        
        # Handle different headless modes
        if cls.HEADLESS_MODE == "auto":
            # Auto-detect based on environment
            if cls.is_ci_mode():
                return cls.CI_HEADLESS
            return cls.HEADLESS
        elif cls.HEADLESS_MODE == "true":
            return True
        elif cls.HEADLESS_MODE == "false":
            return False
        elif cls.HEADLESS_MODE == "debug":
            return False  # Always show browser in debug mode
        else:
            # Fallback to legacy behavior
            if cls.is_ci_mode():
                return cls.CI_HEADLESS
            return cls.HEADLESS
    
    @classmethod
    def get_simple_headless_mode(cls):
        """Get simple headless mode (true/false only)."""
        return cls.RUN_HEADLESS
    
    @classmethod
    def should_record_video_for_failure(cls):
        """Check if video should be recorded for failed tests only."""
        return cls.VIDEO_RECORDING and cls.VIDEO_ON_FAILURE and cls.VIDEO_FAILED_TESTS_ONLY
    
    @classmethod
    def should_take_screenshot_for_failure(cls):
        """Check if screenshot should be taken for failed tests only."""
        return cls.SCREENSHOT_ON_FAILURE and cls.SCREENSHOT_FAILED_TESTS_ONLY
    
    @classmethod
    def get_browser_launch_options(cls):
        """Get browser launch options with enhanced headless control."""
        headless = cls.get_headless_mode()
        
        launch_options = {
            "headless": headless,
            "args": cls.get_browser_args()
        }
        
        # Add debug options if in debug mode
        if cls.HEADLESS_MODE == "debug" or cls.HEADLESS_DEBUG:
            launch_options["devtools"] = True
            launch_options["slow_mo"] = cls.HEADLESS_SLOW_MO
        
        return launch_options

# Global config instance
config = Config()