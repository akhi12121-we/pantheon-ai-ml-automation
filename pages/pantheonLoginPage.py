#!/usr/bin/env python3
"""
Pantheon Page Object Model for Patheon Application.
Contains locators and methods for Patheon  Portal login and navigation.
Provides reusable functions for username entry, password entry, and complete login flow.
"""
import sys
import os
from playwright.async_api import Page, expect
from utils.logger import logger

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from config.settings import config

class PantheonLogin:
    """Page Object Model for Pantheon Portal."""
    
    # ===========================================
    # LOCATORS
    # ===========================================
    USERNAME_FIELD = "input[name='identifier']"
    PASSWORD_FIELD = "input[name='credentials.passcode']"
    NEXT_BUTTON = "input[type='submit'][value='Next']"
    NEXT_BUTTON_ALT = "input[value='Next']"
    VERIFY_BUTTON = "input[type='submit'][value='Verify']"
    AUTHENTICATE_BUTTON = "input[type='submit'][value='Authenticate']"
    
    def __init__(self, page: Page):
        """Initialize the DeveloperPage with a Playwright page object."""
        self.page = page
    
    async def enter_username(self, username: str) -> None:
        """
        Enter username in the username field.
        
        Args:
            username (str): The username to enter
        """
        try:
            logger.info(f"Entering username: {username}")
            await self.page.fill(self.USERNAME_FIELD, username)
            logger.info("Username entered successfully")
        except Exception as e:
            logger.error(f"Failed to enter username: {e}")
            raise
    
    async def enter_password(self, password: str) -> None:
        """
        Enter password in the password field.
        
        Args:
            password (str): The password to enter
        """
        try:
            logger.info("Entering password")
            await self.page.fill(self.PASSWORD_FIELD, password)
            logger.info("Password entered successfully")
        except Exception as e:
            logger.error(f"Failed to enter password: {e}")
            raise
    
    async def click_next(self) -> None:
        """
        Click the Next button.
        """
        try:
            logger.info("Clicking Next button")
            
            # Debug: Check what buttons are available on the page
            try:
                buttons = await self.page.locator("input[type='submit']").all()
                logger.info(f"Found {len(buttons)} submit buttons on page")
                for i, button in enumerate(buttons):
                    value = await button.get_attribute("value")
                    logger.info(f"Button {i}: value='{value}'")
            except Exception as debug_e:
                logger.warning(f"Debug check failed: {debug_e}")
            
            # Try primary locator first
            try:
                await self.page.click(self.NEXT_BUTTON, timeout=5000)
                logger.info("Next button clicked successfully with primary locator")
            except Exception as e1:
                logger.warning(f"Primary locator failed: {e1}")
                # Try alternative locator
                try:
                    await self.page.click(self.NEXT_BUTTON_ALT, timeout=5000)
                    logger.info("Next button clicked successfully with alternative locator")
                except Exception as e2:
                    logger.error(f"Both locators failed. Primary: {e1}, Alternative: {e2}")
                    raise e2
                    
        except Exception as e:
            logger.error(f"Failed to click Next button: {e}")
            raise
    
    async def click_verify(self) -> None:
        """
        Click the Verify button.
        """
        try:
            logger.info("Clicking Verify button")
            await self.page.click(self.VERIFY_BUTTON)
            logger.info("Verify button clicked successfully")
        except Exception as e:
            logger.error(f"Failed to click Verify button: {e}")
            raise
    
    async def click_authenticate(self) -> None:
        """
        Click the Authenticate button.
        
        This function clicks the Authenticate button that appears when URL is launched.
        """
        try:
            logger.info("Clicking Authenticate button")
            await self.page.click(self.AUTHENTICATE_BUTTON)
            logger.info("Authenticate button clicked successfully")
        except Exception as e:
            logger.error(f"Failed to click Authenticate button: {e}")
            raise
    
    async def login(self, username: str, password: str) -> None:
        """
        Complete login process for Patheon application.
        
        Args:
            username (str): The username to login with
            password (str): The password to login with
        """
        try:
            logger.info("Starting Patheon login process")
            
            # Step 0: Click Authenticate button first
            await self.click_authenticate()
            
            # Step 1: Enter username
            await self.enter_username(username)
            await self.click_next()
            
            # Step 2: Enter password
            await self.enter_password(password)
            
            # Step 3: Verify login
            await self.click_verify()
            
            logger.info("Patheon login completed successfully")
        except Exception as e:
            logger.error(f"Patheon login failed: {e}")
            raise
