#!/usr/bin/env python3
"""
XTM Project Manager Page Object Model.
Contains locators and methods for XTM Project Manager login and navigation.
"""
import sys
import os
from playwright.async_api import Page, expect
from utils.logger import logger

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from config.settings import config

class XTMProjectPage:
    """Page Object Model for XTM Project Manager."""
    
    # ===========================================
    # LOCATORS
    # ===========================================
    
    # Login Page Locators
    USERNAME_FIELD = "input[type='text']"
    PASSWORD_FIELD = "input[type='password']"
    LOGIN_BUTTON = "button[type='submit']"
    
    # Project Page Locators
    PROJECTS_IFRAME = "#projectsIframe"
    PROJECTS_HEADING = "h1.page-title"
    ADD_PROJECT_BUTTON = "#SUBMENU_CREATE_PROJECT"
    ADD_PROJECT_HEADING = "h1.tab-title"
    CUSTOMER_DROPDOWN = "table.xmlintl-form-table select#create-project_formProject_customerId"
    PROJECT_NAME_FIELD = "td.input input#projectName"
    SOURCE_LANGUAGE_DROPDOWN = "td.input select#create-project_formProject_project_sourceLanguage"
    TARGET_LANGUAGES_SELECT = "td.input select#tgtAllLangs"
    MOVE_RIGHT_ARROW = "td.input span#multiselect-move-rightselectBoxGroup0"
    FILE_UPLOAD_FIELD = "xpath=//input[@id='formProject.fileForTranslation0']"
    WORKFLOW_DROPDOWN = "xpath=//select[@id='create-project_formProject_project_workflowDefinitionId']"
    CREATE_BUTTON = "table.actions td#create-project-button button"
    
    # ===========================================
    # CONSTRUCTOR
    # ===========================================
    
    def __init__(self, page: Page):
        """Initialize the page object with a Playwright page instance."""
        self.page = page
    
    # ===========================================
    # NAVIGATION METHODS
    # ===========================================
    
    async def navigate_to_login(self):
        """Navigate to XTM Project Manager login page."""
        logger.info("Navigating to XTM login page")
        await self.page.goto(config.XTM_URL)
        await self.page.wait_for_load_state("networkidle")
        logger.info("Successfully navigated to XTM login page")
    
    # ===========================================
    # LOGIN METHODS
    # ===========================================
    
    async def enter_username(self, username):
        """Enter username in the login form."""
        logger.info("Entering username")
        username_field = self.page.locator(self.USERNAME_FIELD)
        await username_field.fill(username)
        logger.info("Username entered successfully")
    
    async def enter_password(self, password):
        """Enter password in the login form."""
        logger.info("Entering password")
        password_field = self.page.locator(self.PASSWORD_FIELD)
        await password_field.fill(password)
        logger.info("Password entered successfully")
    
    async def click_login_button(self):
        """Click the login button."""
        logger.info("Clicking login button")
        login_button = self.page.locator(self.LOGIN_BUTTON)
        await login_button.click()
        await self.page.wait_for_timeout(10000)  # Wait like in recorded script
        logger.info("Login button clicked, waiting for navigation...")
    
    async def login(self, username, password):
        """Perform complete login process."""
        logger.info("Starting login process")
        await self.enter_username(username)
        await self.enter_password(password)
        await self.click_login_button()
        logger.info("Login process completed")
    
    # ===========================================
    # VERIFICATION METHODS
    # ===========================================
    
    async def verify_projects_heading_visible(self):
        """Verify Projects heading is visible after login."""
        logger.info("Verifying Projects heading is visible")
        
        # Wait for iframe to be ready
        await self.page.wait_for_selector(self.PROJECTS_IFRAME, timeout=15000)
        
        # Get the iframe content
        iframe = self.page.frame_locator(self.PROJECTS_IFRAME)
        
        # Check if Projects heading is visible
        projects_heading = iframe.locator(self.PROJECTS_HEADING)
        await expect(projects_heading).to_be_visible(timeout=10000)
        logger.info("Projects heading is visible - login successful")
    
    # ===========================================
    # COMPLETE WORKFLOW METHODS
    # ===========================================
    
    async def complete_login_workflow(self, username, password):
        """Complete login workflow with verification."""
        logger.info("Starting XTM login workflow")
        
        # Navigate to login page
        await self.navigate_to_login()
        
        # Perform login
        await self.login(username, password)
        
        # Verify login success
        await self.verify_projects_heading_visible()
        logger.info("XTM login workflow completed successfully")
    
    async def click_add_project_button(self):
        """Check if Add project button is visible and click it."""
        logger.info("Checking if Add project button is visible")
        
        # Wait for iframe to be ready
        await self.page.wait_for_selector(self.PROJECTS_IFRAME, timeout=10000)
        
        # Get the iframe content
        iframe = self.page.frame_locator(self.PROJECTS_IFRAME)
        
        # Check if Add project button is visible and click it
        add_button = iframe.locator(self.ADD_PROJECT_BUTTON)
        await expect(add_button).to_be_visible(timeout=10000)
        logger.info("Add project button is visible")
        
        await add_button.click()
        logger.info("Add project button clicked successfully")
    
    async def verify_add_project_heading_visible(self):
        """Verify Add project heading is visible."""
        logger.info("Verifying Add project heading is visible")
        
        # Wait for iframe to be ready
        await self.page.wait_for_selector(self.PROJECTS_IFRAME, timeout=10000)
        
        # Get the iframe content
        iframe = self.page.frame_locator(self.PROJECTS_IFRAME)
        
        # Check if Add project heading is visible
        add_heading = iframe.locator(self.ADD_PROJECT_HEADING)
        await expect(add_heading).to_be_visible(timeout=10000)
        logger.info("Add project heading is visible")
    
    async def select_nvidia_customer(self):
        """Verify customer dropdown is visible and select Nvidia_MT_test."""
        logger.info("Verifying customer dropdown is visible")
        
        # Wait for iframe to be ready
        await self.page.wait_for_selector(self.PROJECTS_IFRAME, timeout=10000)
        
        # Get the iframe content
        iframe = self.page.frame_locator(self.PROJECTS_IFRAME)
        
        # Check if customer dropdown is visible
        dropdown = iframe.locator(self.CUSTOMER_DROPDOWN)
        await expect(dropdown).to_be_visible(timeout=20000)
        logger.info("Customer dropdown is visible")
        
        # Select Nvidia_MT_test option
        await dropdown.select_option(label="Nvidia_MT_test")
        logger.info("Selected Nvidia_MT_test from dropdown")
    
    async def enter_project_name(self, project_name):
        """Verify project name field is visible and type value."""
        logger.info("Verifying project name field is visible")
        
        # Wait for iframe to be ready
        await self.page.wait_for_selector(self.PROJECTS_IFRAME, timeout=10000)
        
        # Get the iframe content
        iframe = self.page.frame_locator(self.PROJECTS_IFRAME)
        
        # Check if project name field is visible
        project_field = iframe.locator(self.PROJECT_NAME_FIELD)
        await expect(project_field).to_be_visible(timeout=10000)
        logger.info("Project name field is visible")
        
        # Type the project name
        await project_field.fill(project_name)
        logger.info(f"Entered project name: {project_name}")
    
    async def select_source_language(self):
        """Verify source language dropdown is visible and select English (USA)."""
        logger.info("Verifying source language dropdown is visible")
        
        # Wait for iframe to be ready
        await self.page.wait_for_selector(self.PROJECTS_IFRAME, timeout=10000)
        
        # Get the iframe content
        iframe = self.page.frame_locator(self.PROJECTS_IFRAME)
        
        # Check if source language dropdown is visible
        dropdown = iframe.locator(self.SOURCE_LANGUAGE_DROPDOWN)
        await expect(dropdown).to_be_visible(timeout=10000)
        logger.info("Source language dropdown is visible")
        
        # Select English (USA) option
        await dropdown.select_option(label="English (USA)")
        logger.info("Selected English (USA) from source language dropdown")
    
    async def select_german_target_language(self):
        """Verify target languages select is visible and select German (Germany) and French (France)."""
        logger.info("Verifying target languages select is visible")
        
        # Wait for iframe to be ready
        await self.page.wait_for_selector(self.PROJECTS_IFRAME, timeout=10000)
        
        # Get the iframe content
        iframe = self.page.frame_locator(self.PROJECTS_IFRAME)
        
        # Check if target languages select is visible
        target_select = iframe.locator(self.TARGET_LANGUAGES_SELECT)
        await expect(target_select).to_be_visible(timeout=10000)
        logger.info("Target languages select is visible")
        
        # Get the move arrow locator
        move_arrow = iframe.locator(self.MOVE_RIGHT_ARROW)
                
        # Select French (France) option
        await target_select.select_option(label="French (France)")
        logger.info("Selected French (France) from target languages")
        await move_arrow.click()
        logger.info("Moved French (France) to selected languages")
    
    async def upload_file(self, file_path):
        """Wait for upload field to be visible and upload file."""
        logger.info("Waiting for upload field to be visible")
        
        # Wait for iframe to be ready
        await self.page.wait_for_selector(self.PROJECTS_IFRAME, timeout=10000)
        
        # Get the iframe content
        iframe = self.page.frame_locator(self.PROJECTS_IFRAME)
        
        # Check if upload field is visible
        upload_field = iframe.locator(self.FILE_UPLOAD_FIELD)
        await expect(upload_field).to_be_visible(timeout=10000)
        logger.info("Upload field is visible")
        
        # Upload the file
        await upload_field.set_input_files(file_path)
        logger.info(f"File uploaded successfully: {file_path}")
    
    async def select_workflow(self):
        """Wait for workflow dropdown to be visible and select Translate # Correct."""
        logger.info("Waiting for workflow dropdown to be visible")
        
        # Wait for iframe to be ready
        await self.page.wait_for_selector(self.PROJECTS_IFRAME, timeout=10000)
        
        # Get the iframe content
        iframe = self.page.frame_locator(self.PROJECTS_IFRAME)
        
        # Check if workflow dropdown is visible
        workflow_dropdown = iframe.locator("table.main-text td.input select#create-project_formProject_project_workflowDefinitionId")
        await expect(workflow_dropdown).to_be_visible(timeout=10000)
        logger.info("Workflow dropdown is visible")
        
        # Select Translate # Correct option using value
        await workflow_dropdown.select_option(value="2976")
        await self.page.wait_for_timeout(5000)
        logger.info("Selected Translate # Correct from workflow dropdown")
    
    async def click_create_button(self):
        """Wait for Create button to be visible and click it."""
        logger.info("Waiting for Create button to be visible")
        
        # Wait for iframe to be ready
        await self.page.wait_for_selector(self.PROJECTS_IFRAME, timeout=10000)
        
        # Get the iframe content
        iframe = self.page.frame_locator(self.PROJECTS_IFRAME)
        
        # Check if Create button is visible
        create_button = iframe.locator(self.CREATE_BUTTON)
        await expect(create_button).to_be_visible(timeout=10000)
        logger.info("Create button is visible")
        
        # Click the Create button
        await create_button.click()
        logger.info("Create button clicked successfully")
    
    async def create_xtm_project(self, project_name, file_path):
        """Create XTM project by calling all required functions in sequence."""
        logger.info("Starting XTM project creation workflow")
        
        # Click Add project button
        await self.click_add_project_button()
        await self.page.wait_for_timeout(3000)
        
        # Verify Add project heading is visible
        await self.verify_add_project_heading_visible()
        await self.page.wait_for_timeout(2000)
        
        # Select customer
        await self.select_nvidia_customer()
        await self.page.wait_for_timeout(2000)
        
        # Enter project name
        await self.enter_project_name(project_name)
        await self.page.wait_for_timeout(2000)
        
        # Select source language
        await self.select_source_language()
        await self.page.wait_for_timeout(2000)
        
        # Select target language
        await self.select_german_target_language()
        await self.page.wait_for_timeout(2000)
        
        # Upload file
        await self.upload_file(file_path)
        await self.page.wait_for_timeout(3000)
        
        # Select workflow
        await self.select_workflow()
        await self.page.wait_for_timeout(2000)
        
        # Click Create button
        await self.click_create_button()
        await self.page.wait_for_timeout(5000)
        
        logger.info("XTM project creation workflow completed")
