#!/usr/bin/env python3
"""
Simple UI test to verify Playwright integration.
"""
import pytest
import pytest_asyncio
import asyncio
import sys
import os
import time
from config.settings import config

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from utils.browser_client import browser_client
from utils.logger import logger
from utils.allure_helper import allure_helper

@pytest_asyncio.fixture(scope="function")
async def browser_setup():
    """Setup browser for each test."""
    await browser_client.start_browser()
    yield
    await browser_client.close_browser()

@pytest.mark.asyncio
async def test_apollo_health_page(browser_setup):
    """Test navigating to Apollo health page."""
    test_name = "test_apollo_health_page"
    start_time = time.time()
    logger.log_test_start(test_name)
    
    try:
        # Navigate to Apollo health endpoint
        await browser_client.navigate_to("https://apollo.welocalize.io/health")
        
        # Get page title
        title = await browser_client.get_page_title()
        print(f"Page title: {title}")
        
        # Get current URL
        url = await browser_client.get_current_url()
        print(f"Current URL: {url}")
        
        # Take screenshot
        screenshot_path = await browser_client.take_screenshot("apollo_health_page")
        print(f"Screenshot saved: {screenshot_path}")
        
        # Verify we're on the right page
        assert "apollo.welocalize.io" in url
        assert "health" in url
        
        logger.log_test_end(test_name, "PASSED")
        
        # Generate Allure result
        allure_helper.generate_test_result(
            test_name=test_name,
            status="passed",
            start_time=start_time,
            end_time=time.time()
        )
        
    except Exception as e:
        # Generate failed Allure result
        allure_helper.generate_test_result(
            test_name=test_name,
            status="failed",
            start_time=start_time,
            end_time=time.time(),
            error_message=str(e)
        )
        raise

@pytest.mark.asyncio
async def test_google_search(browser_setup):
    """Test basic Google search functionality."""
    test_name = "test_google_search"
    start_time = time.time()
    logger.log_test_start(test_name)
    
    try:
        # Navigate to Google
        await browser_client.navigate_to(config.PatheonURL)
        
        # Wait for search box
        # await browser_client.wait_for_element("input[name='q']")
        
        # # Fill search box
        # await browser_client.fill("input[name='q']", "Playwright automation")
        
        # # Press Enter to search
        # await browser_client.page.press("input[name='q']", "Enter")
        
        # # Wait for results
        # await browser_client.wait_for_element("#search")
        
        # # Take screenshot
        # screenshot_path = await browser_client.take_screenshot("google_search_results")
        # print(f"Screenshot saved: {screenshot_path}")
        
        # # Verify search results
        # current_url = await browser_client.get_current_url()
        # assert "google.com/search" in current_url
        # assert "q=Playwright+automation" in current_url
        
        logger.log_test_end(test_name, "PASSED")
        
        # Generate Allure result
        allure_helper.generate_test_result(
            test_name=test_name,
            status="passed",
            start_time=start_time,
            end_time=time.time()
        )
        
    except Exception as e:
        # Generate failed Allure result
        allure_helper.generate_test_result(
            test_name=test_name,
            status="failed",
            start_time=start_time,
            end_time=time.time(),
            error_message=str(e)
        )
        raise
