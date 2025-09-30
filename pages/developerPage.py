#!/usr/bin/env python3
"""
Developer Page Object Model.
Contains locators and methods for Developer Portal navigation and job creation.
Provides reusable functions for clicking Create Job button and other developer actions.
"""
import sys
import os
import json
import asyncio
from datetime import datetime
import time
from _pytest.stash import T
from playwright.async_api import Page, expect

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.logger import logger

class DeveloperPage:
    """Page Object Model for Developer Portal."""
    
    # ===========================================
    # LOCATORS
    # ===========================================
    CREATE_JOB_BUTTON = "button:has-text('Create Job')"
    JSON_TEXTAREA = "div.ace_active-line"
    REFRESH_BUTTON = "button.btn.btn-right"
    SUBMIT_BUTTON = "a.btn.blue.submit"
    FIRST_JOB_ROW = "table.jobs-list tbody tr.job-row:first-child"
    JOB_ROW_CREATED_DATE = "table.jobs-list tbody tr.job-row:first-child td:nth-child(3)"
    JOB_ROW_STATUS = "table.jobs-list tbody tr.job-row:first-child td:last-child"
    
    def __init__(self, page: Page):
        """
        Initialize the DeveloperPage with a Playwright page object.
        
        Args:
            page (Page): Playwright page object
        """
        self.page = page
    
    async def navigate_to_developer_page(self, url: str) -> None:
        """
        Navigate to the developer page.
        
        This function navigates to the specified developer page URL.
        
        Args:
            url (str): The URL to navigate to
        """
        try:
            logger.info(f"Navigating to developer page: {url}")
            await self.page.goto(url)
            logger.info("Successfully navigated to developer page")
        except Exception as e:
            logger.error(f"Failed to navigate to developer page: {e}")
            raise
    
    async def click_create_job(self) -> None:
        """
        Click the Create Job button.
        
        This function clicks the Create Job button to navigate to job creation page.
        """
        try:
            logger.info("Clicking Create Job button")
            await self.page.click(self.CREATE_JOB_BUTTON)
            logger.info("Create Job button clicked successfully")
        except Exception as e:
            logger.error(f"Failed to click Create Job button: {e}")
            raise
    
    async def type_json_payload(self, json_file_path: str = "data/api/requests/pullProjectXTM.json") -> None:
        """
        Type JSON payload into the text field.
        
        This function loads JSON data from file and types it into the JSON editor textarea.
        
        Args:
            json_file_path (str): Path to the JSON file to load and type
        """
        try:
            logger.info(f"Loading JSON from file: {json_file_path}")
            
            # Load JSON file
            with open(json_file_path, 'r') as file:
                json_data = json.load(file)
            
            # Convert to formatted JSON string
            json_string = json.dumps(json_data, indent=2)
            logger.info(f"JSON content: {json_string}")
            
            # Debug: Check if textarea exists
            try:
                textarea_count = await self.page.locator("textarea").count()
                logger.info(f"Found {textarea_count} textarea elements")
            except Exception as debug_e:
                logger.warning(f"Debug check failed: {debug_e}")
            
            logger.info("Typing JSON payload into text field")
            await self.page.fill(self.JSON_TEXTAREA, json_string)
            logger.info("JSON payload typed successfully")
            
        except Exception as e:
            logger.error(f"Failed to type JSON payload: {e}")
            raise
    
    async def type_json_direct(self, json_string: str) -> None:
        """
        Type JSON string directly into the text field using simple approach.
        
        This function uses the simple locator approach to fill the JSON text field.
        
        Args:
            json_string (str): The JSON string to type
        """
        try:
            logger.info(f"Typing JSON directly: {json_string}")
            
            # Use the simple approach with modal textbox
            logger.info("Filling JSON text field using simple locator")
            await self.page.locator("#create-modal").get_by_role("textbox").clear()
            await self.page.locator("#create-modal").get_by_role("textbox").type(json_string)
            logger.info("JSON payload typed successfully")
            
        except Exception as e:
            logger.error(f"Failed to type JSON payload: {e}")
            raise
    
    async def click_refresh(self) -> None:
        """
        Click the Refresh button.
        
        This function clicks the Refresh button to refresh the current page or data.
        """
        try:
            logger.info("Clicking Refresh button")
            await self.page.click(self.REFRESH_BUTTON)
            logger.info("Refresh button clicked successfully")
        except Exception as e:
            logger.error(f"Failed to click Refresh button: {e}")
            raise
    
    async def verify_new_job_row(self, expected_platform_id: str = "446", timeout: int = 10) -> bool:
        """
        Verify that a new job row appears in the top 5 rows with current date and expected status.
        
        This function checks the top 5 rows for:
        - A row with current date (contains today's date)
        - Status shows "Success on platformInstanceId [expected_platform_id]"
        
        Args:
            expected_platform_id (str): Expected platform instance ID in the status
            timeout (int): Maximum time to wait for the table (seconds)
            
        Returns:
            bool: True if verification passes, False otherwise
        """
        try:
            logger.info(f"Verifying new job row with platform ID [{expected_platform_id}]")
            
            # Wait for the table to be visible
            await self.page.wait_for_selector("table.jobs-list", timeout=timeout * 1000)
            logger.info("Jobs table found")
            
            # Get current date and time in table format
            now = datetime.now()
            current_date = now.strftime("%#m/%d/%y")  # e.g., "9/25/25"
            current_time = now.strftime("%#I:%M:%S %p").lower()  # e.g., "1:57:03 pm"
            
            logger.info(f"Looking for current date: {current_date} and time around: {current_time}")
            
            # Check top 5 rows only
            for row_num in range(1, 6):
                try:
                    # Get date from current row
                    date_selector = f"table.jobs-list tbody tr.job-row:nth-child({row_num}) td:nth-child(3)"
                    date_text = await self.page.text_content(date_selector)
                    
                    # Get status from current row
                    status_selector = f"table.jobs-list tbody tr.job-row:nth-child({row_num}) td:last-child"
                    status_text = await self.page.text_content(status_selector)
                    
                    logger.info(f"Row {row_num} - Date: {date_text}, Status: {status_text}")
                    
                    # Simple check: current date in text AND expected status
                    has_current_date = current_date in date_text
                    has_expected_status = f"Success on platformInstanceId [{expected_platform_id}]" in status_text
                    
                    if has_current_date and has_expected_status:
                        logger.info(f"Found matching row {row_num} with current date and expected status")
                        logger.info("New job row verification completed successfully")
                        return True
                        
                except Exception as e:
                    logger.warning(f"Could not read row {row_num}: {e}")
                    continue
            
            logger.warning("No matching row found in top 5 rows")
            return False
                
        except Exception as e:
            logger.error(f"Failed to verify new job row: {e}")
            return False
    
    async def click_submit(self) -> None:
        """
        Click the Submit button to submit the payload.
        
        This function clicks the Submit button to submit the JSON payload.
        """
        try:
            logger.info("Clicking Submit button")
            await self.page.click(self.SUBMIT_BUTTON)
            logger.info("Submit button clicked successfully")
        except Exception as e:
            logger.error(f"Failed to click Submit button: {e}")
            raise
    
    async def complete_job_creation_flow(self, url: str, username: str, password: str, json_file_path: str = "data/api/requests/pullProjectXTM.json", expected_platform_id: str = "446") -> bool:
        """
        Complete job creation flow with navigation and login.
        
        This function performs the complete flow:
        1. Navigate to developer page
        2. Login with credentials
        3. Click Create Job button
        4. Type JSON payload
        5. Click Submit button
        6. Wait for submission
        7. Click Refresh button
        8. Wait for refresh
        9. Verify new job row appears
        
        Args:
            url (str): URL to navigate to
            username (str): Username for login
            password (str): Password for login
            json_file_path (str): Path to the JSON file to load and type
            expected_platform_id (str): Expected platform instance ID in the status
            
        Returns:
            bool: True if complete flow succeeds, False otherwise
        """
        try:
            logger.info("Starting complete job creation flow with navigation and login")
            
            # Step 1: Navigate to developer page
            logger.info("Step 1: Navigating to developer page")
            await self.navigate_to_developer_page(url)
            
            # Step 2: Login with credentials
            logger.info("Step 2: Logging in with credentials")
            from pages.pantheonLoginPage import PantheonLogin
            pantheon_login = PantheonLogin(self.page)
            await pantheon_login.login(username, password)
            
            # Step 3: Click Create Job button
            time.sleep(5)
            await self.page.wait_for_load_state("networkidle")
            logger.info("Step 3: Clicking Create Job button")
            await self.click_create_job()
            
            # Step 4: Type JSON payload
            logger.info("Step 4: Typing JSON payload")
            await self.type_json_direct('{"platformInstanceId": 446}')
            time.sleep(5)
            # Step 5: Click Submit button
            logger.info("Step 5: Clicking Submit button")
            await self.click_submit()
            time.sleep(5)
            
            # Step 6: Wait for submission to complete
            logger.info("Step 6: Waiting for submission to complete (5 seconds)")
            await asyncio.sleep(10)
            
            # Step 7: Click Refresh button
            logger.info("Step 7: Clicking Refresh button")
            await self.click_refresh()
            
            # Step 8: Wait for refresh to complete
            logger.info("Step 8: Waiting for refresh to complete (3 seconds)")
            await asyncio.sleep(3)
            
            # Step 9: Verify new job row appears
            logger.info("Step 9: Verifying new job row appears")
            is_verified = await self.verify_new_job_row(expected_platform_id)
            
            if is_verified:
                logger.info("Complete job creation flow completed successfully")
                return True
            else:
                logger.error("Complete job creation flow failed - verification failed")
                return False
                
        except Exception as e:
            logger.error(f"Complete job creation flow failed: {e}")
            return False
        
        
