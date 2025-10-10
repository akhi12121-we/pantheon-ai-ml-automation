#!/usr/bin/env python3
"""
Test Search Project Relay - Search for a project using the relay page.
"""
import pytest
import pytest_asyncio
import sys
import os
from utils.logger import logger

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from utils.browser_client import browser_client
from utils.data_parser import data_parser
from pages.relayPage import RelayPage

@pytest_asyncio.fixture(scope="function")
async def browser_setup():
    """Setup browser for each test."""
    await browser_client.start_browser(headless=False, args=['--ignore-certificate-errors', '--ignore-ssl-errors', '--ignore-certificate-errors-spki-list'])
    yield
    await browser_client.close_browser()

@pytest.mark.asyncio
async def test_search_project_relay(browser_setup):
    """Test searching for a project using the relay page."""
    logger.info("Starting Test Search Project Relay")
    
    try:
        # Read project name from file using utility function
        project_name = data_parser.read_project_name()
        logger.info(f"Using project name: {project_name}")
        
        # Create relay page object
        relay_page = RelayPage(browser_client.page)
        
        # Call the search_project_name function
        success = await relay_page.search_project_name(
            search_term=project_name,
            expected_text=project_name
        )
        
        # Assert the result
        assert success, f"Test Search Project Relay failed - search_project_name returned False for project: {project_name}"
        logger.info("Test Search Project Relay completed successfully!")
        
    except Exception as e:
        logger.error(f"Test Search Project Relay failed with exception: {e}")
        raise
