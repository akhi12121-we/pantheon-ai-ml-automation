#!/usr/bin/env python3
"""
XTM Project Manager UI Test - Simple login and verify heading.
"""
import pytest
import pytest_asyncio
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from utils.browser_client import browser_client
from utils.config_parser import get_config_value
from config.settings import config
from pages.xtm_project_page import XTMProjectPage

@pytest_asyncio.fixture(scope="function")
async def browser_setup():
    """Setup browser for each test."""
    await browser_client.start_browser(headless=False)
    yield
    await browser_client.close_browser()

@pytest.mark.asyncio
async def test_xtm_login_and_verify_heading(browser_setup):
    """Test login to XTM and verify Projects heading."""
    # Load credentials using utility
    username = get_config_value("credentials", "username")
    password = get_config_value("credentials", "password")
    
    xtm_page = XTMProjectPage(browser_client.page)
    await xtm_page.complete_login_workflow(username, "#Zbb<h5Ec5h&")