#!/usr/bin/env python3
"""
XTM Project Creation Test - Create a new project using the page object.
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
from pages.xtm_project_page import XTMProjectPage

@pytest_asyncio.fixture(scope="function")
async def browser_setup():
    """Setup browser for each test."""
    await browser_client.start_browser(headless=False)
    yield
    await browser_client.close_browser()

@pytest.mark.projectcreation
@pytest.mark.asyncio
async def test_01_create_xtm_project(browser_setup):
    """Test creating a new XTM project."""
    # Load credentials and project data from config
    username = get_config_value("credentials", "username", "xtm_data.ini")
    password = get_config_value("credentials", "password", "xtm_data.ini")
    project_name = get_config_value("xtm_project_data", "project_name", "xtm_data.ini") + " " + datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = get_config_value("xtm_project_data", "file_path", "xtm_data.ini")
    logger.info(f"Creating project: {project_name}")
    logger.info(f"File path: {file_path}")
    # Create page object
    xtm_page = XTMProjectPage(browser_client.page)
    
    # Complete login workflow first
    await xtm_page.complete_login_workflow(username, password)
    
    # Create the project
    await xtm_page.create_xtm_project(project_name, file_path)
    
    # Write project name to file for API tests
    with open("data/projectname.txt", "w") as f:
        f.write(project_name)