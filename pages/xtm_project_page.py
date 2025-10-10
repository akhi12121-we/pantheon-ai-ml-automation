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
    
    # Search Locators
    SEARCH_INPUT_FIELD = "input#searchValue"
    PROJECT_ROW_BY_NAME = "tr[data-projectname='{project_name}']"
    PROJECT_NAME_CELL = "td.projects_table_NAME"
    
    # Workflow Locators
    WORKFLOW_LINK = "a#workflow_id"
    
    # Manage Jobs Section Locators
    MANAGE_JOBS_BUTTON = "button[id='manageAllJobs'][name='manageAllJobs']"
    MANAGE_JOBS_BUTTON_ALT = "button:has-text('Manage jobs')"
    MANAGE_JOBS_BUTTON_CSS = "button._button_1dqou_157._ghost_1dqou_228._small_1dqou_277"
    MANAGE_JOBS_BUTTON_DATA_TESTID = "button[data-tesid='manageAllJobsButton']"
    MANAGE_JOBS_BUTTON_EXACT_TEXT = "button:has-text('Manage jobs')"
    
    # File Context Menu Locators
    TESTFILE_CELL = "td._tableCell_1ovga_180:has-text('TestFile_965Words.docx')"
    TESTFILE_CELL_ALT = "td:has-text('TestFile_965Words.docx')"
    TESTFILE_CELL_GENERIC = "td[class*='tableCell']:has-text('TestFile_965Words.docx')"
    OPEN_WORKBENCH_MENU = "li#JOB_CONTEXT_MENU_WORKBENCH_POPUP_94371837 a"
    READONLY_CHECKBOX = "input#readOnlyWorkbenchCheckbox"
    OPEN_BUTTON = "button#popupOpenWorkbenchOpenButton"
    
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
        await self.page.wait_for_load_state('networkidle')
        await self.page.wait_for_timeout(10000)
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
                
        # Select German (Germany) option
        await target_select.select_option(label="German (Germany)")
        logger.info("Selected German (Germany) from target languages")
        await move_arrow.click()
        logger.info("Moved German (Germany) to selected languages")
    
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
        """
        Create XTM project by calling all required functions in sequence.
        
        PROJECT CREATION WORKFLOW STEPS:
        ================================
        Step 1: Click Add project button
        Step 2: Verify Add project heading is visible
        Step 3: Select Nvidia customer from dropdown
        Step 4: Enter project name in text field
        Step 5: Select English (USA) as source language
        Step 6: Select German (Germany) as target language
        Step 7: Upload file for translation
        Step 8: Select Translate # Correct workflow
        Step 9: Click Create button to create project
        Step 10: Wait for project creation to complete
        
        Args:
            project_name (str): Name of the project to create
            file_path (str): Path to the file to upload for translation
        """
        logger.info("Starting XTM project creation workflow")
        
        # Step 1: Click Add project button
        await self.click_add_project_button()
        await self.page.wait_for_timeout(3000)
        
        # Step 2: Verify Add project heading is visible
        await self.verify_add_project_heading_visible()
        await self.page.wait_for_timeout(2000)
        
        # Step 3: Select customer
        await self.select_nvidia_customer()
        await self.page.wait_for_timeout(2000)
        
        # Step 4: Enter project name
        await self.enter_project_name(project_name)
        await self.page.wait_for_timeout(2000)
        
        # Step 5: Select source language
        await self.select_source_language()
        await self.page.wait_for_timeout(2000)
        
        # Step 6: Select target language
        await self.select_german_target_language()
        await self.page.wait_for_timeout(2000)
        
        # Step 7: Upload file
        await self.upload_file(file_path)
        await self.page.wait_for_timeout(3000)
        
        # Step 8: Select workflow
        await self.select_workflow()
        await self.page.wait_for_timeout(2000)
        
        # Step 9: Click Create button
        await self.click_create_button()
        await self.page.wait_for_timeout(5000)
        
        logger.info("XTM project creation workflow completed")
    
    # ===========================================
    # SEARCH METHODS
    # ===========================================
    
    async def search_xtm_project(self, projectname):
        """
        Search for a project in XTM using the search functionality.
        
        Args:
            projectname (str): The name of the project to search for
            
        Returns:
            bool: True if search was successful, False otherwise
        """
        logger.info(f"Starting search for project: {projectname}")
        
        try:
            # Wait for iframe to be ready
            await self.page.wait_for_selector(self.PROJECTS_IFRAME, timeout=15000)
            logger.info("Projects iframe is ready")
            
            # Get the iframe content
            iframe = self.page.frame_locator(self.PROJECTS_IFRAME)
            
            # Wait for search input field to be visible
            search_field = iframe.locator(self.SEARCH_INPUT_FIELD)
            await expect(search_field).to_be_visible(timeout=10000)
            logger.info("Search input field is visible")
            
            # Clear any existing text and enter search term
            await search_field.clear()
            await search_field.fill(projectname)
            logger.info(f"Entered search term: {projectname}")
            
            # Press Enter to trigger search
            await search_field.press("Enter")
            logger.info("Search triggered with Enter key")
            
            # Wait a moment for search results to load
            await self.page.wait_for_timeout(7000)
            logger.info("Search completed successfully")
            
            return True
            
        except Exception as e:
            logger.error(f"Error occurred during project search: {str(e)}")
            return False
    
    async def verify_project_and_click(self, project_name):
        """
        Verify project exists in search results and click on it.
        
        Args:
            project_name (str): The name of the project to verify and click
            
        Returns:
            bool: True if project was found and clicked successfully, False otherwise
        """
        logger.info(f"Verifying and clicking on project: {project_name}")
        
        try:
            # Wait for iframe to be ready
            await self.page.wait_for_selector(self.PROJECTS_IFRAME, timeout=15000)
            logger.info("Projects iframe is ready")
            
            # Get the iframe content
            iframe = self.page.frame_locator(self.PROJECTS_IFRAME)
            
            # Create locator for project row using data-projectname attribute
            project_row_locator = iframe.locator(self.PROJECT_ROW_BY_NAME.format(project_name=project_name))
            
            # Wait for project row to be visible
            await expect(project_row_locator).to_be_visible(timeout=10000)
            logger.info(f"Project row found for: {project_name}")
            
            # Verify project name in the cell
            project_name_cell = project_row_locator.locator(self.PROJECT_NAME_CELL)
            await expect(project_name_cell).to_be_visible(timeout=5000)
            logger.info(f"Project name cell is visible for: {project_name}")
            
            # Click on the project row
            await project_row_locator.click()
            logger.info(f"Successfully clicked on project: {project_name}")
            
            # Wait a moment for navigation
            await self.page.wait_for_timeout(3000)
            logger.info("Project click completed successfully")
            
            return True
            
        except Exception as e:
            logger.error(f"Error occurred while verifying and clicking project: {str(e)}")
            return False
    
    # ===========================================
    # WORKFLOW METHODS
    # ===========================================
    
    async def click_workflow(self):
        """
        Click on the Workflow link using recorded locator.
        
        Returns:
            bool: True if workflow link was clicked successfully, False otherwise
        """
        logger.info("Clicking on Workflow link")
        
        try:
            await self.page.wait_for_load_state("networkidle")
            await self.page.frame_locator('#projectsIframe').get_by_text('Workflow', exact=True).click()
            # Wait for navigation to complete
            await self.page.wait_for_timeout(3000)
            await self.page.wait_for_load_state("networkidle")
            
            logger.info("Workflow link clicked successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error occurred while clicking workflow link: {str(e)}")
            return False

    
    async def click_manage_Jobs_section(self):
        """
        Click on the Manage jobs button using recorded locator.
        
        Returns:
            bool: True if manage jobs button was clicked successfully, False otherwise
        """
        logger.info("Clicking on Manage jobs button")
        
        # Wait for the iframe to be ready first
        await self.page.wait_for_selector('#projectsIframe', timeout=10000)
        
        # Wait for the nested iframes to load
        await self.page.wait_for_timeout(2000)
        
        # Click the Manage jobs button
        await self.page.frame_locator('#projectsIframe').frame_locator('#newWorkflowIframe').frame_locator('#projecteditorworkIframe').get_by_role('button', name='Manage jobs').click()
        
        # Wait for navigation to complete
        await self.page.wait_for_timeout(2000)
        
        logger.info("Manage jobs button clicked successfully")
        return True
        
    
       
    # ===========================================
    # VERIFICATION METHODS
    # ===========================================
    
    async def verify_lock_icon(self, page=None):
        """
        Verify lock icon exists in the page.
        
        Args:
            page: Optional page object to check. If None, uses self.page
        
        Returns:
            bool: True if lock icon is found, False otherwise
        """
        target_page = page if page else self.page
        logger.info("Verifying lock icon in the page")
        
        # Look for lock icon using the correct locator
        lock_icon_locator = "i.fa.fa-lock"
        
        # Check if lock icon exists
        lock_icons = target_page.locator(lock_icon_locator)
        count = await lock_icons.count()
        
        if count > 0:
            logger.info(f"Found {count} lock icon(s) in the page")
            return True
        else:
            logger.info("No lock icons found in the page")
            return False
    
    # ===========================================
    # DEBUG METHODS
    # ===========================================
    
    async def dump_workflow_html(self, iframe=None):
        """
        Dump HTML content for debugging purposes.
        
        Args:
            iframe: Optional iframe locator, if None uses main page
            
        Returns:
            str: Path to the dumped HTML file
        """
        try:
            import time
            import os
            
            # Create directory if it doesn't exist
            dump_dir = "data/ui/testdata"
            os.makedirs(dump_dir, exist_ok=True)
            
            html_file = os.path.join(dump_dir, "dumpWorkflow.html")
            
            # Get the source to dump
            if iframe:
                page_source = await iframe.locator("html").inner_html()
            else:
                page_source = await self.page.content()
            
            # Write simple HTML dump
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(f"<!-- HTML Dump - {time.strftime('%Y-%m-%d %H:%M:%S')} -->\n")
                f.write(page_source)
            
            logger.info(f"HTML dumped to {html_file}")
            return html_file
            
        except Exception as e:
            logger.error(f"Failed to dump HTML: {str(e)}")
            return None

    # ===========================================
    # FILE CONTEXT MENU METHODS
    # ===========================================
    
    async def right_click_and_redirect_segment_section(self):
        """
        Right-click on TestFile_965Words.docx using recorded locator.
        
        Returns:
            str: URL of the new tab if successful, False if error occurred
        """
        logger.info("Starting right-click workflow for TestFile_965Words.docx")
        
        # Use the exact recorded locator for right-click
        await self.page.frame_locator('#projectsIframe').frame_locator('#newWorkflowIframe').frame_locator('#projecteditorworkIframe').get_by_text('TestFile_965Words.docx').click(button='right')
        
        logger.info("Right-clicked on TestFile_965Words.docx")
        
        # Click "Open XTM Workbench" menu item
        await self.page.frame_locator('#projectsIframe').frame_locator('#newWorkflowIframe').frame_locator('#projecteditorworkIframe').get_by_role('menuitem', name=' Open XTM Workbench').click()
        
        logger.info("Clicked on 'Open XTM Workbench' menu item")
        
        # Uncheck read-only checkbox
        await self.page.frame_locator('#projectsIframe').frame_locator('#newWorkflowIframe').frame_locator('#projecteditorworkIframe').get_by_role('checkbox', name='Read-only').uncheck()
        
        logger.info("Unchecked read-only checkbox")
        
        # Wait for popup event
        page1_promise = self.page.wait_for_event('popup')
        
        # Click Open button
        await self.page.frame_locator('#projectsIframe').frame_locator('#newWorkflowIframe').frame_locator('#projecteditorworkIframe').get_by_role('button', name='Open').click()
        
        # Get the new page
        page1 = await page1_promise
        
        logger.info("Right-click workflow completed successfully")
        
        # Return the new page URL
        new_url = page1.url
        logger.info(f"New tab URL: {new_url}")
        return new_url
    
    # ===========================================
    # COMPREHENSIVE WORKFLOW METHODS
    # ===========================================
    
    async def searchProject_click_segment(self, username, password, projectName):
        """
        Comprehensive workflow to search project and navigate to segment section.
        
        WORKFLOW STEPS:
        ==============
        1. Login into XTM application
        2. Search project (parameterized)
        3. Wait for search results
        4. Verify project row and click
        5. Wait for project to load
        6. Click workflow tab
        7. Wait for workflow to load
        8. Click manage jobs section
        9. Wait for manage jobs section to load
        10. Right-click on file section
        11. Wait for context menu
        12. Verify popup appears
        13. Toggle read-only checkbox
        14. Click OK button
        15. Wait for navigation
        16. Focus on new tab
        
        Args:
            username (str): XTM username for login
            password (str): XTM password for login
            projectName (str): Name of the project to search for
            
        Returns:
            bool: True if workflow completed successfully, False otherwise
        """
        logger.info("Starting comprehensive searchProject_click_segment workflow")
        
        try:
            # Step 1: Login into XTM application
            logger.info("Step 1: Logging into XTM application")
            await self.complete_login_workflow(username, password)
            logger.info("Login completed successfully")
            
            # Step 2: Search project
            logger.info(f"Step 2: Searching for project: {projectName}")
            await self.search_xtm_project(projectName)
            logger.info("Project search completed")
            
            # Step 3: Wait for search results
            logger.info("Step 3: Waiting for search results to load")
            await self.page.wait_for_timeout(3000)
            logger.info("Search results loaded")
            
            # Step 4: Verify project row and click
            logger.info(f"Step 4: Verifying and clicking project: {projectName}")
            await self.verify_project_and_click(projectName)
            logger.info("Project clicked successfully")
            
            # Step 5: Wait for project to load
            logger.info("Step 5: Waiting for project to load")
            await self.page.wait_for_timeout(5000)
            logger.info("Project loaded")
            
            # Step 6: Click workflow tab
            logger.info("Step 6: Clicking workflow tab")
            await self.click_workflow()
            logger.info("Workflow tab clicked")
            
            # Step 7: Wait for workflow to load
            logger.info("Step 7: Waiting for workflow to load")
            await self.page.wait_for_timeout(10000)
            logger.info("Workflow loaded")
            
            # Step 8: Click manage jobs section
            logger.info("Step 8: Clicking manage jobs section")
            await self.click_manage_Jobs_section()
            logger.info("Manage jobs section clicked")
            
            # Step 9: Wait for manage jobs section to load
            logger.info("Step 9: Waiting for manage jobs section to load")
            await self.page.wait_for_timeout(3000)
            logger.info("Manage jobs section loaded")
            
            # Step 10: Right-click on file section
            logger.info("Step 10: Right-clicking on file section")
            newtab = await self.right_click_and_redirect_segment_section()
            logger.info(f"Right-click on file section completed to new tab: {newtab}")
            
            # Step 11: Wait for context menu
            logger.info("Step 11: Waiting for context menu")
            await self.page.wait_for_timeout(2000)
            logger.info("Context menu processed")
            
            # Step 15: Wait for navigation
            logger.info("Step 15: Waiting for navigation to complete")
            await self.page.wait_for_timeout(15000)
            logger.info("Navigation completed")
            
            # Step 16: Focus on new tab
            logger.info("Step 16: Focusing on new tab")
            # Get all pages and focus on the latest one (new tab)
            pages = self.page.context.pages
            if len(pages) > 1:
                new_page = pages[-1]
                await new_page.bring_to_front()
                await new_page.wait_for_load_state("networkidle")
                await new_page.wait_for_timeout(30000)
                logger.info("Focused on new tab successfully")
                
                # Step 17: Verify lock icon in new tab
                logger.info("Step 17: Verifying lock icon in new tab")
                lock_icon_found = await self.verify_lock_icon(new_page)
                if lock_icon_found:
                    logger.info("Lock icon verification successful")
                else:
                    logger.error("Lock icon verification failed")
                    return False  # Fail the test if lock icon verification fails
            else:
                logger.info("No new tab detected, staying on current page")
            
            logger.info("Comprehensive searchProject_click_segment workflow completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error occurred during comprehensive workflow: {str(e)}")
            return False
        
        