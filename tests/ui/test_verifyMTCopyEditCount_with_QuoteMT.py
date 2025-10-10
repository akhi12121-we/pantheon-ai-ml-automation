#!/usr/bin/env python3
"""
Test Verify MT Copy Edit Count with Quote MT - Verify MT count is less than Copy Edit MT count.
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
async def test_verify_mt_count_less_than_copy_edit_mt_count(browser_setup):
    """Test verifying MT count is less than Copy Edit MT count."""
    logger.info("Starting Test Verify MT Copy Edit Count with Quote MT")
    
    try:
        # Read project name from file using utility function
        project_name = data_parser.read_project_name()
        logger.info(f"Using project name: {project_name}")
        
        # Create relay page object
        relay_page = RelayPage(browser_client.page)
        
        # Call the verify_mt_count_less_then_copyEdit_MT_count function
        success = await relay_page.verify_mt_count_less_then_copyEdit_MT_count(
            project_name=project_name
        )
        
        # Assert the result
        assert success, f"Test Verify MT Copy Edit Count with Quote MT failed - verify_mt_count_less_then_copyEdit_MT_count returned False for project: {project_name}"
        logger.info("Test Verify MT Copy Edit Count with Quote MT completed successfully!")
        
    except Exception as e:
        logger.error(f"Test Verify MT Copy Edit Count with Quote MT failed with exception: {e}")
        raise
