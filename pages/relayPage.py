#!/usr/bin/env python3
"""
Relay Page Object Model.
Contains locators and methods for Relay Portal navigation.
"""
import sys
import os
from playwright.async_api import Page, expect

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.logger import logger
from config.settings import config
from pages.pantheonLoginPage import PantheonLogin
from utils.config_parser import get_config_value

class RelayPage:
    """Page Object Model for Relay Portal."""
    
    # ===========================================
    # LOCATORS
    # ===========================================
    WELOCALIZE_LOGIN_BUTTON = "button[data-test='login-button']"
    USERNAME_INPUT = "input[name='identifier']"
    PASSWORD_INPUT = "input[name='credentials.passcode']"
    NEXT_BUTTON = "input[data-type='save']"
    VERIFY_BUTTON = "input[data-type='save'][value='Verify']"
    PROJECT_LINK = "span:has-text('Projects')"
    ALL_PROJECTS_TAB = "li.tab:has-text('All projects')"
    SEARCH_INPUT = "input[placeholder='Search by project, client, client reference ID, or status']"
    PROJECT_ROW = "tr"
    PROJECT_LINK_DYNAMIC = "a[href*='/project/']"
    
    def __init__(self, page: Page):
        """
        Initialize the RelayPage with a Playwright page object.
        
        Args:
            page (Page): Playwright page object
        """
        self.page = page
    
    async def click_welocalize_login_button(self) -> None:
        """
        Click the Welocalize login button.
        
        This function clicks the Welocalize login button after the page loads.
        """
        try:
            logger.info("Clicking Welocalize login button")
            await self.page.click(self.WELOCALIZE_LOGIN_BUTTON)
            logger.info("Welocalize login button clicked successfully")
        except Exception as e:
            logger.error(f"Failed to click Welocalize login button: {e}")
            raise

    async def type_username(self, username: str) -> None:
        """
        Type username in the username input field.
        
        This function types the provided username in the username input field.
        
        Args:
            username (str): The username to type
        """
        try:
            logger.info(f"Typing username: {username}")
            await self.page.fill(self.USERNAME_INPUT, username)
            logger.info("Username typed successfully")
        except Exception as e:
            logger.error(f"Failed to type username: {e}")
            raise

    async def type_password(self, password: str) -> None:
        """
        Type password in the password input field.
        
        This function types the provided password in the password input field.
        
        Args:
            password (str): The password to type
        """
        try:
            logger.info("Typing password")
            await self.page.fill(self.PASSWORD_INPUT, password)
            logger.info("Password typed successfully")
        except Exception as e:
            logger.error(f"Failed to type password: {e}")
            raise

    async def click_next_button(self) -> None:
        """
        Click the Next button.
        
        This function clicks the Next button to proceed to the next step.
        """
        try:
            logger.info("Clicking Next button")
            await self.page.click(self.NEXT_BUTTON)
            logger.info("Next button clicked successfully")
        except Exception as e:
            logger.error(f"Failed to click Next button: {e}")
            raise

    async def click_verify_button(self) -> None:
        """
        Click the Verify button.
        
        This function clicks the Verify button after password entry.
        """
        try:
            logger.info("Clicking Verify button")
            await self.page.click(self.VERIFY_BUTTON)
            logger.info("Verify button clicked successfully")
        except Exception as e:
            logger.error(f"Failed to click Verify button: {e}")
            raise

    async def navigate_to_relay_page(self) -> None:
        """
        Navigate to the relay page.
        
        This function navigates to the relay page using the configured URL.
        """
        try:
            url = config.SEARCH_PULLED_PROJECT_URL
            logger.info(f"Navigating to relay page: {url}")
            await self.page.goto(url)
            await self.page.wait_for_timeout(2000)  # Wait for page to load
            logger.info("Successfully navigated to relay page")
        except Exception as e:
            logger.error(f"Failed to navigate to relay page: {e}")
            raise
    
    async def click_project_link(self) -> None:
        """
        Click the Project link.
        
        This function clicks the Project link to navigate to projects page.
        """
        try:
            logger.info("Clicking Project link")
            await self.page.click(self.PROJECT_LINK)
            logger.info("Project link clicked successfully")
        except Exception as e:
            logger.error(f"Failed to click Project link: {e}")
            raise
    
    async def click_all_projects_tab(self) -> None:
        """
        Click the All projects tab.
        
        This function clicks the All projects tab to view all projects.
        """
        try:
            logger.info("Clicking All projects tab")
            await self.page.click(self.ALL_PROJECTS_TAB)
            logger.info("All projects tab clicked successfully")
        except Exception as e:
            logger.error(f"Failed to click All projects tab: {e}")
            raise
    
    async def search_project(self, search_term: str) -> None:
        """
        Search for a project using the search input.
        
        This function enters the search term in the search input field.
        
        Args:
            search_term (str): The term to search for
        """
        try:
            logger.info(f"Searching for project: {search_term}")
            await self.page.fill(self.SEARCH_INPUT, search_term)
            await self.page.keyboard.press("Enter")
            logger.info(f"Successfully entered search term: {search_term}")
        except Exception as e:
            logger.error(f"Failed to search for project: {e}")
            raise
    
    async def verify_project_row(self, expected_text: str) -> bool:
        """
        Verify that a project row contains the expected text.
        
        This function checks if any project row contains the expected text.
        
        Args:
            expected_text (str): The text to verify in the project row
            
        Returns:
            bool: True if the text is found, False otherwise
        """
        try:
            logger.info(f"Verifying project row contains: {expected_text}")
            
            # Get all project rows
            rows = await self.page.locator(self.PROJECT_ROW).all()
            
            for row in rows:
                row_text = await row.text_content()
                if expected_text in row_text:
                    logger.info(f"Found matching project row: {expected_text}")
                    return True
            
            logger.warning(f"No project row found containing: {expected_text}")
            return False
            
        except Exception as e:
            logger.error(f"Failed to verify project row: {e}")
            return False
    
    async def click_first_project_link(self) -> None:
        """
        Click on the first project link found in the table.
        
        This function clicks on the first available project link.
        """
        try:
            logger.info("Clicking on the first project link")
            await self.page.click("a[href*='/project/']")
            logger.info("Successfully clicked project link")
        except Exception as e:
            logger.error(f"Failed to click project link: {e}")
            raise
    
    async def search_project_name(self, search_term: str, expected_text: str) -> bool:
        """
        Complete workflow to search for a project name.
        
        This function performs the complete workflow:
        1. Navigate to relay page
        2. Login with credentials
        3. Click Projects link
        4. Click All projects tab
        5. Search for project
        6. Verify project row
        7. Click on project link
        
        Args:
            search_term (str): Term to search for
            expected_text (str): Expected text to verify in project row
            
        Returns:
            bool: True if complete workflow succeeds, False otherwise
        """
        try:
            logger.info("Starting complete project search workflow")
            
            # Get credentials from config
            username = get_config_value('pantheon_login_data', 'username', 'pantheon_data.ini')
            password = get_config_value('pantheon_login_data', 'password', 'pantheon_data.ini')
            
            # Step 1: Navigate to relay page
            logger.info("Step 1: Navigating to relay page")
            await self.navigate_to_relay_page()
            await self.page.wait_for_load_state("networkidle")
            await self.click_welocalize_login_button()
            await self.page.wait_for_load_state("networkidle")
            
            
            # Step 2: Login with credentials
            logger.info("Step 2: Logging in with credentials")
            await self.type_username(username)
            await self.click_next_button()
            await self.page.wait_for_load_state("networkidle")
            await self.type_password(password)
            await self.click_verify_button()
            await self.page.wait_for_load_state("networkidle")
            await self.page.wait_for_timeout(3000)
            
            # Step 3: Click Projects link
            logger.info("Step 3: Clicking Projects link")
            await self.click_project_link()
            await self.page.wait_for_timeout(2000)
            
            # Step 4: Click All projects tab
            logger.info("Step 4: Clicking All projects tab")
            await self.click_all_projects_tab()
            await self.page.wait_for_timeout(2000)
            
            # Step 5: Search for project
            logger.info("Step 5: Searching for project")
            await self.search_project(search_term)
            await self.page.wait_for_timeout(7000)
            
            # Step 6: Verify project row
            logger.info("Step 6: Verifying project row")
            is_verified = await self.verify_project_row(expected_text)
            if not is_verified:
                logger.error("Project row verification failed")
                return False
            
            # Step 7: Click on project link
            logger.info("Step 7: Clicking on project link")
            await self.click_first_project_link()
            await self.page.wait_for_load_state("networkidle")
            await self.page.wait_for_timeout(5000)
            
            logger.info("Complete project search workflow completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Complete project search workflow failed: {e}")
            return False
