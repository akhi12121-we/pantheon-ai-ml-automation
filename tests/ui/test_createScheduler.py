#!/usr/bin/env python3
"""
Test Create Scheduler - Create a new job using the developer page.
"""
import pytest
import pytest_asyncio
import sys
import os
from datetime import datetime
from utils.logger import logger

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from utils.browser_client import browser_client
from utils.config_parser import get_config_value
from pages.developerPage import DeveloperPage
from pages.pantheonLoginPage import PantheonLogin
from config.settings import config

@pytest_asyncio.fixture(scope="function")
async def browser_setup():
    """Setup browser for each test."""
    await browser_client.start_browser(headless=False, args=['--ignore-certificate-errors', '--ignore-ssl-errors', '--ignore-certificate-errors-spki-list'])
    yield
    await browser_client.close_browser()

@pytest.mark.asyncio
async def test_create_scheduler(browser_setup):
    """Test creating a new scheduler job."""
    logger.info("Starting Test Create Scheduler")
    
    # Get credentials and URL
    username = get_config_value('pantheon_login_data', 'username', 'pantheon_data.ini')
    password = get_config_value('pantheon_login_data', 'password', 'pantheon_data.ini')
    url = config.PULL_PROJECT_URL
    
    logger.info(f"Using URL: {url}")
    logger.info(f"Using username: {username}")
    
    # Create developer page object
    developer_page = DeveloperPage(browser_client.page)
    
    # Call the complete job creation flow function
    success = await developer_page.complete_job_creation_flow(
        url=url,
        username=username,
        password=password
    )
    
    # Assert the result
    assert success, "Test Create Scheduler failed - complete_job_creation_flow returned False"
    logger.info("Test Create Scheduler completed successfully!")
