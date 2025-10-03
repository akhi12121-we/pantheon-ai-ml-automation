#!/usr/bin/env python3
"""
Test AI Task Verification - Verify all AI-related task completions.
"""
import pytest
import pytest_asyncio
import sys
import os
from utils.logger import logger

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from utils.browser_client import browser_client
from pages.relayPage import RelayPage

@pytest_asyncio.fixture(scope="function")
async def browser_setup():
    """Setup browser for each test."""
    await browser_client.start_browser(headless=False, args=['--ignore-certificate-errors', '--ignore-ssl-errors', '--ignore-certificate-errors-spki-list'])
    yield
    await browser_client.close_browser()

def read_project_name():
    """Read project name from projectname.txt file."""
    try:
        project_name_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'projectname.txt')
        with open(project_name_path, 'r', encoding='utf-8') as file:
            project_name = file.read().strip()
            logger.info(f"Read project name from file: {project_name}")
            return project_name
    except Exception as e:
        logger.error(f"Failed to read project name from file: {e}")
        raise

@pytest.mark.asyncio
async def test_verify_ai_task_completion(browser_setup):
    """Test verifying all AI-related task completions."""
    logger.info("Starting Test Verify AI Task Completion")
    
    try:
        # Read project name from file
        project_name = read_project_name()
        logger.info(f"Using project name: {project_name}")
        
        # Create relay page object
        relay_page = RelayPage(browser_client.page)
        
        # Call the verify_completion_ai_related_tasks function
        await relay_page.verify_completion_ai_related_tasks(project_name)
        
        logger.info("Test Verify AI Task Completion completed successfully!")
        
    except Exception as e:
        logger.error(f"Test Verify AI Task Completion failed with exception: {e}")
        raise
