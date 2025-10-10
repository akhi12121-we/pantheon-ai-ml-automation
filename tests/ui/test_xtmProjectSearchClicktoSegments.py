#!/usr/bin/env python3
"""
XTM Project Search and Segment Navigation Test - Search for a project and navigate to segments.
"""
import pytest
import pytest_asyncio
import sys
import os
from utils.logger import logger

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from utils.browser_client import browser_client
from utils.config_parser import get_config_value
from pages.xtm_project_page import XTMProjectPage

@pytest_asyncio.fixture(scope="function")
async def browser_setup():
    """Setup browser for each test."""
    await browser_client.start_browser(headless=False)
    yield
    await browser_client.close_browser()

@pytest.mark.projectsearch
@pytest.mark.asyncio
async def test_01_search_project_and_click_segments(browser_setup):
    """Test searching for a project and navigating to segments."""
    # Load credentials from config
    username = get_config_value("credentials", "username", "xtm_data.ini")
    password = get_config_value("credentials", "password", "xtm_data.ini")
    
    # Read project name from file
    with open("data/projectname.txt", "r") as f:
        project_name = f.read().strip()
    
    logger.info(f"Searching for project: {project_name}")
    
    # Create page object
    xtm_page = XTMProjectPage(browser_client.page)
    
    # Call the comprehensive workflow function
    result = await xtm_page.searchProject_click_segment(username, password, project_name)
    
    # Assert the workflow completed successfully
    assert result == True, "Project search and segment navigation workflow failed"
    logger.info("Project search and segment navigation completed successfully")
