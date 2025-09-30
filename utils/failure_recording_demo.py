#!/usr/bin/env python3
"""
Demo utility to demonstrate failure-only screenshot and video recording.
This file shows how to use the browser_client utilities for recording test failures.
"""
import pytest
import pytest_asyncio
import asyncio
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.browser_client import browser_client
from utils.logger import logger
from config.settings import config

@pytest_asyncio.fixture(scope="function")
async def browser_setup():
    """Setup browser for each test."""
    await browser_client.start_browser()
    yield
    await browser_client.close_browser()

@pytest.mark.asyncio
async def demo_successful_navigation(browser_setup):
    """Demo successful navigation - should not record video/screenshot if configured for failures only."""
    logger.log_test_start("demo_successful_navigation")

    # Navigate to health endpoint using config
    health_url = f"{config.APOLLO_URL}/health"
    await browser_client.navigate_to(health_url)

    # Assertions
    page_title = await browser_client.get_page_title()
    current_url = await browser_client.get_current_url()
    logger.info(f"Page title: {page_title}")
    logger.info(f"Current URL: {current_url}")

    assert config.APOLLO_URL in current_url
    assert "health" in current_url

    # Take screenshot (should be skipped if configured for failures only)
    screenshot_path = await browser_client.take_screenshot("successful_navigation", test_failed=False)
    if screenshot_path:
        logger.info(f"Screenshot taken for successful test: {screenshot_path}")
    else:
        logger.info("Screenshot skipped for successful test (configured for failures only)")

    # Save video (should be skipped if configured for failures only)
    video_path = await browser_client.save_video("successful_navigation", test_failed=False)
    if video_path:
        logger.info(f"Video saved for successful test: {video_path}")
    else:
        logger.info("Video recording skipped for successful test (configured for failures only)")

    logger.log_test_end("demo_successful_navigation", "PASSED")

@pytest.mark.asyncio
async def demo_failed_navigation(browser_setup):
    """Demo failed navigation - should record video/screenshot if configured for failures only."""
    logger.log_test_start("demo_failed_navigation")

    try:
        # Navigate to a non-existent page to trigger failure using config
        non_existent_url = f"{config.APOLLO_URL}/non-existent-page"
        await browser_client.navigate_to(non_existent_url)

        # This assertion will fail
        page_title = await browser_client.get_page_title()
        assert "Non-existent" in page_title, "This should fail to demonstrate failure recording"

    except Exception as e:
        logger.error(f"Test failed as expected: {e}")
        
        # Take screenshot for failed test
        screenshot_path = await browser_client.take_screenshot("failed_navigation", test_failed=True)
        if screenshot_path:
            logger.info(f"Screenshot taken for failed test: {screenshot_path}")
        else:
            logger.info("Screenshot skipped for failed test (not configured)")

        # Save video for failed test
        video_path = await browser_client.save_video("failed_navigation", test_failed=True)
        if video_path:
            logger.info(f"Video saved for failed test: {video_path}")
        else:
            logger.info("Video recording skipped for failed test (not configured)")

        # Re-raise the exception to mark test as failed
        raise

    logger.log_test_end("demo_failed_navigation", "FAILED")

@pytest.mark.asyncio
async def demo_headless_mode_demonstration(browser_setup):
    """Demo to demonstrate different headless modes."""
    logger.log_test_start("demo_headless_mode_demonstration")

    # Navigate to a page using config
    health_url = f"{config.APOLLO_URL}/health"
    await browser_client.navigate_to(health_url)

    # Get current headless mode
    headless_mode = config.get_headless_mode()
    headless_setting = config.HEADLESS_MODE
    
    logger.info(f"Current headless mode: {headless_mode}")
    logger.info(f"Headless setting: {headless_setting}")
    logger.info(f"Browser type: {config.BROWSER_TYPE}")

    # Take a screenshot to show the current state
    screenshot_path = await browser_client.take_screenshot("headless_demo", test_failed=False)
    if screenshot_path:
        logger.info(f"Demo screenshot saved: {screenshot_path}")

    logger.log_test_end("demo_headless_mode_demonstration", "PASSED")
