#!/usr/bin/env python3
"""
Relay Page Object Model.
Contains locators and methods for Relay Portal navigation.
"""
import sys
import os
import re
from playwright.async_api import Page, expect
import time

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
    PRODUCTION_STATUS = ".production-status-container span[title='Production']"
    PRODUCTION_BADGE = ".badge:has-text('Production')"
    TIMELINE_LINK = "a[href*='/timeline']"
    ANALYSIS_CHECK_ICON = ".timeline-col .icon-check-thick"
    DROPDOWN_ARROW = ".dropdown-container .icon-chevron-down"
    HISTORY_OPTION = ".dropdown-dialog .option-list div:has-text('History')"
    
    # Task verification locators
    FILE_UPLOAD_TASK = "div[class*='File upload'].cta-item.activity-card .lead"
    INTAKE_TASK = ".intake.cta-item.activity-card .lead"
    ANALYSIS_TASK = ".analysis.cta-item.activity-card .lead"
    SCOPING_TASK = ".scoping.cta-item.activity-card .lead"
    QUOTE_SUBMIT_TASK = ".quote-submit.cta-item.activity-card .lead"
    APPROVAL_TASK = ".approval.cta-item.activity-card h4"
    CONFIRM_INTAKE_KIT_TASK = ".confirm-intake-kit.cta-item.activity-card .lead"
    MAP_TASK_ASSET_TASK = ".map-task-asset.cta-item.activity-card .lead"
    PLANNING_TASK = ".planning.cta-item.activity-card .lead"
    AI_QUALITY_ESTIMATE_TASK = ".GetXLIFF.files.cta-item.activity-card .lead"
    AI_GET_AI_POST_EDITING_TASK = ".Get_AIPE.cta-item.activity-card .lead"
    AI_GET_QUALITY_ESTIMATE_TASK = ".Get_AIQE.cta-item.activity-card .lead"
    LOCK_SEGMENTS_AIQE_TASK = ".Lock_Segments_AIQE.cta-item.activity-card .lead"
    UPLOAD_BILINGUAL_FILE_TASK = ".Upload_Bilingual_File_AIQE.cta-item.activity-card .lead"
    UPDATE_SCOPE_AIQE_TASK = ".Update_Scope_AIQE.cta-item.activity-card .lead"
    AIQE_CALCULATION_TASK = ".ai-quality-estimate.cta-item.activity-card .lead"
    
    # Task heading locators
    FILE_UPLOAD_HEADING = "div[class*='File upload'].cta-item.activity-card h4"
    INTAKE_HEADING = ".intake.cta-item.activity-card h4"
    ANALYSIS_HEADING = ".analysis.cta-item.activity-card h4"
    SCOPING_HEADING = ".scoping.cta-item.activity-card h4"
    QUOTE_SUBMIT_HEADING = ".quote-submit.cta-item.activity-card h4"
    APPROVAL_HEADING = ".approval.cta-item.activity-card h4"
    CONFIRM_INTAKE_KIT_HEADING = ".confirm-intake-kit.cta-item.activity-card h4"
    MAP_TASK_ASSET_HEADING = ".map-task-asset.cta-item.activity-card h4"
    PLANNING_HEADING = ".planning.cta-item.activity-card h4"
    AI_QUALITY_ESTIMATE_HEADING = ".GetXLIFF.files.cta-item.activity-card h4"
    AI_GET_AI_POST_EDITING_HEADING = ".Get_AIPE.cta-item.activity-card h4"
    AI_GET_QUALITY_ESTIMATE_HEADING = ".Get_AIQE.cta-item.activity-card h4"
    LOCK_SEGMENTS_AIQE_HEADING = ".Lock_Segments_AIQE.cta-item.activity-card h4"
    UPLOAD_BILINGUAL_FILE_HEADING = ".Upload_Bilingual_File_AIQE.cta-item.activity-card h4"
    UPDATE_SCOPE_AIQE_HEADING = ".Update_Scope_AIQE.cta-item.activity-card h4"
    AIQE_CALCULATION_HEADING = ".ai-quality-estimate.cta-item.activity-card h4"
    
    COMPLETION_MESSAGE = "This task was completed by"
    RIGHT_ARROW = ".pagination-controls .icon-arrow-right"
    DISABLED_RIGHT_ARROW = ".pagination-controls .disabled.icon-arrow-right"
    
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
    
    async def verify_production_status(self) -> bool:
        """
        Verify that Production status is present in the current row.
        
        This function checks if the production status element contains "Production" text.
        
        Returns:
            bool: True if Production status is found, False otherwise
        """
        try:
            logger.info("Verifying Production status in row")
            
            # Check if production status element exists and contains "Production"
            production_element = self.page.locator(self.PRODUCTION_STATUS)
            
            if await production_element.count() > 0:
                production_text = await production_element.text_content()
                if "Production" in production_text:
                    logger.info("Production status verified successfully")
                    return True
                else:
                    logger.warning(f"Production status element found but text is: {production_text}")
                    return False
            else:
                logger.warning("Production status element not found")
                return False
                
        except Exception as e:
            logger.error(f"Failed to verify Production status: {e}")
            return False
    
    async def verify_production_badge(self) -> bool:
        """
        Verify that Production badge is present.
        
        This function checks if the production badge element contains "Production" text.
        
        Returns:
            bool: True if Production badge is found, False otherwise
        """
        try:
            logger.info("Verifying Production badge")
            
            # Check if production badge element exists and contains "Production"
            production_badge = self.page.locator(self.PRODUCTION_BADGE)
            
            if await production_badge.count() > 0:
                badge_text = await production_badge.text_content()
                if "Production" in badge_text:
                    logger.info("Production badge verified successfully")
                    return True
                else:
                    logger.warning(f"Production badge element found but text is: {badge_text}")
                    return False
            else:
                logger.warning("Production badge element not found")
                return False
                
        except Exception as e:
            logger.error(f"Failed to verify Production badge: {e}")
            return False
    
    async def extract_and_save_project_number(self) -> str:
        """
        Extract project number from current URL and save it to projectNumberId.txt file.
        
        This function extracts the project number from the URL pattern /project/{number}/
        and saves it to a text file named projectNumberId.txt.
        
        Returns:
            str: The extracted project number, or empty string if not found
        """
        try:
            logger.info("Extracting project number from URL")
            
            # Get current URL
            current_url = self.page.url
            logger.info(f"Current URL: {current_url}")
            
            # Extract project number using regex pattern
            pattern = r'/project/(\d+)/'
            match = re.search(pattern, current_url)
            
            if match:
                project_number = match.group(1)
                logger.info(f"Extracted project number: {project_number}")
                
                # Save to file
                file_path = "data/projectNumberId.txt"
                with open(file_path, 'w') as file:
                    file.write(project_number)
                
                logger.info(f"Project number {project_number} saved to {file_path}")
                return project_number
            else:
                logger.warning("No project number found in URL")
                return ""
                
        except Exception as e:
            logger.error(f"Failed to extract and save project number: {e}")
            return ""
    
    async def verify_pulledProject_is_ProductionStatus(self, search_term: str) -> bool:
        """
        Complete workflow to navigate, login, search project, verify production status, 
        and extract project ID.
        
        This function performs the following steps:
        1. Navigate to the URL
        2. Login into the application
        3. Click project
        4. Click All projects
        5. Search project
        6. Verify production in the row
        7. Click to that row project link
        8. Verify production on the next page
        9. Extract project ID and save into the file
        
        Args:
            search_term (str): The project name or term to search for
            
        Returns:
            bool: True if complete workflow succeeds, False otherwise
        """
        try:
            logger.info("Starting complete project workflow")
            
            # Get credentials from config
            username = get_config_value('pantheon_login_data', 'username', 'pantheon_data.ini')
            password = get_config_value('pantheon_login_data', 'password', 'pantheon_data.ini')
            
            # Step 1: Navigate to the URL
            logger.info("Step 1: Navigating to relay page")
            await self.navigate_to_relay_page()
            await self.page.wait_for_load_state("networkidle")
            await self.click_welocalize_login_button()
            await self.page.wait_for_load_state("networkidle")
            
            # Step 2: Login into the application
            logger.info("Step 2: Logging in with credentials")
            await self.type_username(username)
            await self.click_next_button()
            await self.page.wait_for_load_state("networkidle")
            await self.type_password(password)
            await self.click_verify_button()
            await self.page.wait_for_load_state("networkidle")
            await self.page.wait_for_timeout(3000)
            
            # Step 3: Click project
            logger.info("Step 3: Clicking Project link")
            await self.click_project_link()
            await self.page.wait_for_timeout(2000)
            
            # Step 4: Click All projects
            logger.info("Step 4: Clicking All projects tab")
            await self.click_all_projects_tab()
            await self.page.wait_for_timeout(2000)
            
            # Step 5: Search project
            logger.info("Step 5: Searching for project")
            await self.search_project(search_term)
            await self.page.wait_for_timeout(7000)
            
            # Step 6: Verify production in the row
            logger.info("Step 6: Verifying production in the row")
            is_production_verified = await self.verify_production_status()
            if not is_production_verified:
                logger.error("Production status not found in project row")
                return False
            
            # Step 7: Click to that row project link
            logger.info("Step 7: Clicking on project link")
            await self.click_first_project_link()
            await self.page.wait_for_load_state("networkidle")
            await self.page.wait_for_timeout(10000)
            
            # Step 8: Verify production on the next page
            logger.info("Step 8: Verifying production on the next page")
            is_production_badge_verified = await self.verify_production_badge()
            if not is_production_badge_verified:
                logger.error("Production badge not found on project page")
                return False
            
            # Step 9: Extract project ID and save into the file
            logger.info("Step 9: Extracting project ID and saving to file")
            project_number = await self.extract_and_save_project_number()
            if not project_number:
                logger.error("Failed to extract project number")
                return False
            
            logger.info("Complete project workflow completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Complete project workflow failed: {e}")
            return False
    
    async def click_timeline_link(self) -> None:
        """
        Click on the Timeline link.
        
        This function clicks on the Timeline link in the collapsible header.
        """
        try:
            logger.info("Clicking Timeline link")
            await self.page.click(self.TIMELINE_LINK)
            logger.info("Timeline link clicked successfully")
        except Exception as e:
            logger.error(f"Failed to click Timeline link: {e}")
            raise
    
    async def verify_analysis_with_tick_mark(self) -> bool:
        """
        Verify that Analysis has a tick mark (check icon).
        
        This function checks if the Analysis section has a check icon indicating completion.
        
        Returns:
            bool: True if Analysis has tick mark, False otherwise
        """
        try:
            logger.info("Verifying Analysis with tick mark")
            
            # Check if the check icon exists in the timeline
            check_icon = self.page.locator(self.ANALYSIS_CHECK_ICON)
            
            if await check_icon.count() > 0:
                logger.info("Analysis tick mark verified successfully")
                return True
            else:
                logger.warning("Analysis tick mark not found")
                return False
                
        except Exception as e:
            logger.error(f"Failed to verify Analysis tick mark: {e}")
            return False
    
    async def click_dropdown_and_select_history(self) -> None:
        """
        Click the dropdown arrow and select History option.
        
        This function clicks the dropdown arrow and selects the History option from the dropdown menu.
        """
        try:
            logger.info("Clicking dropdown arrow")
            await self.page.click(self.DROPDOWN_ARROW)
            logger.info("Dropdown arrow clicked successfully")
            
            await self.page.wait_for_timeout(2000)
            logger.info("Selecting History option")
            await self.page.click(self.HISTORY_OPTION)
            logger.info("History option selected successfully")
            await self.page.wait_for_timeout(2000)
            
        except Exception as e:
            logger.error(f"Failed to click dropdown and select History: {e}")
            raise
    
    async def _verify_heading(self, heading_locator: str, expected_text: str) -> None:
        """Verify task heading."""
        heading = await self.page.locator(heading_locator).text_content()
        assert expected_text in heading
    
    async def verify_file_upload_completed(self) -> None:
        """Verify File Upload task completion message."""
        await self._verify_heading(self.FILE_UPLOAD_HEADING, "File Upload")
        text = await self.page.locator(self.FILE_UPLOAD_TASK).text_content()
        assert self.COMPLETION_MESSAGE in text
    
    async def verify_intake_completed(self) -> None:
        """Verify Intake task completion message."""
        await self._verify_heading(self.INTAKE_HEADING, "Intake")
        text = await self.page.locator(self.INTAKE_TASK).text_content()
        assert self.COMPLETION_MESSAGE in text
    
    async def click_right_arrow(self) -> None:
        """Click right arrow."""
        await self.page.click(self.RIGHT_ARROW)
    
    async def verify_analysis_completed(self) -> None:
        """Verify Analysis task completion message."""
        await self.click_right_arrow()
        await self.page.wait_for_timeout(2000)
        await self._verify_heading(self.ANALYSIS_HEADING, "Analysis")
        text = await self.page.locator(self.ANALYSIS_TASK).text_content()
        assert self.COMPLETION_MESSAGE in text
    
    async def verify_scoping_completed(self) -> None:
        """Verify Scoping task completion message."""
        await self.click_right_arrow()
        await self.page.wait_for_timeout(2000)
        await self._verify_heading(self.SCOPING_HEADING, "Scoping")
        text = await self.page.locator(self.SCOPING_TASK).text_content()
        assert self.COMPLETION_MESSAGE in text
    
    async def verify_quote_submit_completed(self) -> None:
        """Verify Quote Submission task completion message."""
        await self.click_right_arrow()
        await self.page.wait_for_timeout(2000)
        await self._verify_heading(self.QUOTE_SUBMIT_HEADING, "Quote Submission")
        text = await self.page.locator(self.QUOTE_SUBMIT_TASK).text_content()
        assert self.COMPLETION_MESSAGE in text
    
    async def verify_edit_approve_quote(self) -> None:
        """Verify Edit or Approve Quote text."""
        await self.click_right_arrow()
        await self.page.wait_for_timeout(2000)
        await self._verify_heading(self.APPROVAL_HEADING, "Edit or Approve Quote")
        text = await self.page.locator(self.APPROVAL_TASK).text_content()
        assert "Edit or Approve Quote" in text
    
    async def verify_confirm_intake_kit_completed(self) -> None:
        """Verify Confirm Intake Kit task completion message."""
        await self.click_right_arrow()
        await self.page.wait_for_timeout(2000)
        await self._verify_heading(self.CONFIRM_INTAKE_KIT_HEADING, "Confirm Intake Kit")
        text = await self.page.locator(self.CONFIRM_INTAKE_KIT_TASK).text_content()
        assert self.COMPLETION_MESSAGE in text
    
    async def verify_map_task_asset_completed(self) -> None:
        """Verify Map Task Asset task completion message."""
        await self.click_right_arrow()
        await self.page.wait_for_timeout(2000)
        await self._verify_heading(self.MAP_TASK_ASSET_HEADING, "Map Task Asset")
        text = await self.page.locator(self.MAP_TASK_ASSET_TASK).text_content()
        assert self.COMPLETION_MESSAGE in text
    
    async def verify_planning_completed(self) -> None:
        """Verify Planning task completion message."""
        await self.click_right_arrow()
        await self.page.wait_for_timeout(2000)
        await self._verify_heading(self.PLANNING_HEADING, "Planning")
        text = await self.page.locator(self.PLANNING_TASK).text_content()
        assert self.COMPLETION_MESSAGE in text
    
    async def verify_ai_quality_estimate_completed(self) -> None:
        """Verify AI Quality Estimate XLIFF task completion message."""
        await self.click_right_arrow()
        await self.page.wait_for_timeout(2000)
        await self._verify_heading(self.AI_QUALITY_ESTIMATE_HEADING, "AI Quality Estimate XLIFF")
        text = await self.page.locator(self.AI_QUALITY_ESTIMATE_TASK).text_content()
        assert self.COMPLETION_MESSAGE in text
    
    async def verify_ai_get_ai_post_editing_completed(self) -> None:
        """Verify AI Get AI Post Editing task completion message."""
        await self.click_right_arrow()
        await self.page.wait_for_timeout(2000)
        await self._verify_heading(self.AI_GET_AI_POST_EDITING_HEADING, "AI Get AI Post Editing")
        text = await self.page.locator(self.AI_GET_AI_POST_EDITING_TASK).text_content()
        assert self.COMPLETION_MESSAGE in text
    
    async def verify_ai_get_quality_estimate_completed(self) -> None:
        """Verify AI Get Quality Estimate task completion message."""
        try:
            await self.click_right_arrow()
            await self.page.wait_for_timeout(2000)
            await self._verify_heading(self.AI_GET_QUALITY_ESTIMATE_HEADING, "AI Get Quality Estimate")
            text = await self.page.locator(self.AI_GET_QUALITY_ESTIMATE_TASK).text_content()
            assert self.COMPLETION_MESSAGE in text
        except Exception as e:
            logger.warning(f"AI Get Quality Estimate verification failed (may not be available): {e}")
            # Continue execution - this task might not be available for all projects
    
    async def verify_lock_segments_aiqe_completed(self) -> None:
        """Verify Lock Segments AIQE task completion message."""
        await self.click_right_arrow()
        await self.page.wait_for_timeout(2000)
        await self._verify_heading(self.LOCK_SEGMENTS_AIQE_HEADING, "Lock Segments AIQE")
        text = await self.page.locator(self.LOCK_SEGMENTS_AIQE_TASK).text_content()
        assert self.COMPLETION_MESSAGE in text
    
    async def verify_upload_bilingual_file_completed(self) -> None:
        """Verify Upload Bilingual File task completion message."""
        await self.click_right_arrow()
        await self.page.wait_for_timeout(2000)
        await self._verify_heading(self.UPLOAD_BILINGUAL_FILE_HEADING, "Upload Bilingual File")
        text = await self.page.locator(self.UPLOAD_BILINGUAL_FILE_TASK).text_content()
        assert self.COMPLETION_MESSAGE in text
    
    async def verify_update_scope_aiqe_completed(self) -> None:
        """Verify Update Scope AIQE task completion message."""
        await self.click_right_arrow()
        await self.page.wait_for_timeout(2000)
        await self._verify_heading(self.UPDATE_SCOPE_AIQE_HEADING, "Update Scope AIQE")
        text = await self.page.locator(self.UPDATE_SCOPE_AIQE_TASK).text_content()
        assert self.COMPLETION_MESSAGE in text
    
    async def verify_aiqe_calculation_completed(self) -> None:
        """Verify AIQE Calculation task completion message."""
        await self.click_right_arrow()
        await self.page.wait_for_timeout(2000)
        await self._verify_heading(self.AIQE_CALCULATION_HEADING, "AIQE Calculation")
        text = await self.page.locator(self.AIQE_CALCULATION_TASK).text_content()
        assert self.COMPLETION_MESSAGE in text
        time.sleep(10)        
        # Verify right arrow is disabled
        await self.click_right_arrow()
        await self.page.wait_for_timeout(1000)
        await self.page.wait_for_selector(self.DISABLED_RIGHT_ARROW, timeout=5000)
    
    async def login_to_application(self) -> None:
        """Login to the application using credentials from config."""
        try:
            # Click Welocalize login button
            await self.click_welocalize_login_button()
            await self.page.wait_for_load_state("networkidle")
            
            # Get credentials from config
            username = get_config_value('pantheon_login_data', 'username', 'pantheon_data.ini')
            password = get_config_value('pantheon_login_data', 'password', 'pantheon_data.ini')
            
            logger.info("Logging in with credentials")
            await self.type_username(username)
            await self.click_next_button()
            await self.page.wait_for_load_state("networkidle")
            await self.type_password(password)
            await self.click_verify_button()
            await self.page.wait_for_load_state("networkidle")
            await self.page.wait_for_timeout(3000)
            logger.info("Login completed successfully")
            
        except Exception as e:
            logger.error(f"Login failed: {e}")
            raise
    
    async def verify_completion_ai_related_tasks(self, project_name: str) -> None:
        """
        Complete workflow to verify all AI-related task completions.
        
        This function performs the complete workflow:
        1. Navigate to relay page
        2. Login to application
        3. Click project
        4. Wait for load
        5. Click project all
        6. Wait for load
        7. Search for project
        8. Wait for load
        9. Click project link
        10. Wait for load
        11. Click timeline
        12. Wait to load
        13. Select history
        14. Wait to load
        15. Wait to load
        16-32. Verify all task completions
        
        Args:
            project_name (str): Project name to search for
        """
        try:
            # Step 1: Navigate to relay page
            logger.info("Step 1: Navigating to relay page")
            await self.navigate_to_relay_page()
            await self.page.wait_for_load_state("networkidle")
            
            # Step 2: Login to application
            logger.info("Step 2: Logging in to application")
            await self.login_to_application()

            # Step 3: Click project
            logger.info("Step 3: Clicking project")
            await self.click_project_link()
            
            # Step 4: Wait for load
            logger.info("Step 4: Waiting for load")
            await self.page.wait_for_timeout(3000)
            
            # Step 5: Click project all
            logger.info("Step 5: Clicking project all")
            await self.click_all_projects_tab()
            
            # Step 6: Wait for load
            logger.info("Step 6: Waiting for load")
            await self.page.wait_for_timeout(3000)
            
            # Step 7: Search for project
            logger.info("Step 7: Searching for project")
            await self.search_project(project_name)
            
            # Step 8: Wait for load
            logger.info("Step 8: Waiting for load")
            await self.page.wait_for_timeout(3000)
            
            # Step 9: Click project link
            logger.info("Step 9: Clicking project link")
            await self.click_first_project_link()
            
            # Step 10: Wait for load
            logger.info("Step 10: Waiting for load")
            await self.page.wait_for_timeout(3000)
            
            # Step 11: Click timeline
            logger.info("Step 11: Clicking timeline")
            await self.click_timeline_link()
            
            # Step 12: Wait to load
            logger.info("Step 12: Waiting to load")
            await self.page.wait_for_timeout(3000)
            
            # Step 13: Select history
            logger.info("Step 13: Selecting history")
            await self.click_dropdown_and_select_history()
            
            # Step 14: Wait to load
            logger.info("Step 14: Waiting to load")
            await self.page.wait_for_timeout(3000)
            
            # Step 15: Wait to load
            logger.info("Step 15: Waiting to load")
            await self.page.wait_for_timeout(3000)
            
            # Steps 16-31: Verify all task completions
            logger.info("Steps 16-31: Verifying all task completions")
            
            # Step 16: Verify File Upload
            logger.info("Step 16: Verifying File Upload completion")
            await self.verify_file_upload_completed()
            
            # Step 17: Verify Intake
            logger.info("Step 17: Verifying Intake completion")
            await self.verify_intake_completed()
            
            # Step 18: Click right arrow
            logger.info("Step 18: Clicking right arrow")
            await self.click_right_arrow()
            
            # Step 19: Verify Analysis
            logger.info("Step 19: Verifying Analysis completion")
            await self.verify_analysis_completed()
            
            # Step 20: Verify Scoping
            logger.info("Step 20: Verifying Scoping completion")
            await self.verify_scoping_completed()
            
            # Step 21: Verify Quote Submission
            logger.info("Step 21: Verifying Quote Submission completion")
            await self.verify_quote_submit_completed()
            
            # Step 22: Verify Edit or Approve Quote
            logger.info("Step 22: Verifying Edit or Approve Quote completion")
            await self.verify_edit_approve_quote()
            
            # Step 23: Verify Confirm Intake Kit
            logger.info("Step 23: Verifying Confirm Intake Kit completion")
            await self.verify_confirm_intake_kit_completed()
            
            # Step 24: Verify Map Task Asset
            logger.info("Step 24: Verifying Map Task Asset completion")
            await self.verify_map_task_asset_completed()
            
            # Step 25: Verify Planning
            logger.info("Step 25: Verifying Planning completion")
            await self.verify_planning_completed()
            
            # Step 26: Verify AI Quality Estimate
            logger.info("Step 26: Verifying AI Quality Estimate completion")
            await self.verify_ai_quality_estimate_completed()
            
            # Step 27: Verify AI Get AI Post Editing
            logger.info("Step 27: Verifying AI Get AI Post Editing completion")
            await self.verify_ai_get_ai_post_editing_completed()
            
            # Step 28: Verify AI Get Quality Estimate
            logger.info("Step 28: Verifying AI Get Quality Estimate completion")
            await self.verify_ai_get_quality_estimate_completed()
            
            # Step 29: Verify Lock Segments AIQE
            logger.info("Step 29: Verifying Lock Segments AIQE completion")
            await self.verify_lock_segments_aiqe_completed()
            
            # Step 30: Verify Upload Bilingual File
            logger.info("Step 30: Verifying Upload Bilingual File completion")
            await self.verify_upload_bilingual_file_completed()
            
            # Step 31: Verify Update Scope AIQE
            logger.info("Step 31: Verifying Update Scope AIQE completion")
            await self.verify_update_scope_aiqe_completed()
            
            # Step 32: Verify AIQE Calculation
            logger.info("Step 32: Verifying AIQE Calculation completion")
            await self.verify_aiqe_calculation_completed()
            
            logger.info("All AI-related task verifications completed successfully!")
            
        except Exception as e:
            logger.error(f"AI-related task verification failed: {e}")
            raise
    
