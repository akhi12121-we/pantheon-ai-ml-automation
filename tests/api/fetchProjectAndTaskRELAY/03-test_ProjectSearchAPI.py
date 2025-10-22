"""
Test cases for Project Search API.
"""
import pytest
import json
import os
import requests
from datetime import datetime
from config.settings import config
from utils.logger import logger


class TestProjectSearchAPI:
    """Test class for Project Search API."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test fixtures."""
        self.base_url = "https://hypnos.welocalize.xyz"
        self.endpoint = "/v1/platform-project/"
        
        # Query parameters for the API
        self.query_params = {
            "$limit": 10,
            "$offset": 0,
            "status": "created,new,processing,error,hold,discovered",
            "$order_by": "id",
            "$order_dir": "ASC"
        }
    
    @pytest.mark.projectcreation
    def test_03_project_search_api(self):
        """
        Test fetching projects using platform-project API.
        
        TEST WORKFLOW STEPS:
        ===================
        Step 1: Prepare API headers with authentication
        Step 2: Build full URL with endpoint
        Step 3: Log request details (URL, params, headers)
        Step 4: Make GET request with query parameters
        Step 5: Log response details for debugging
        Step 6: Generate current date for filename
        Step 7: Create response directory if needed
        Step 8: Save response data to JSON file
        Step 9: Verify response status code is 200
        Step 10: Verify response is valid JSON object
        Step 11: Read expected project name from file
        Step 12: Parse response data and count projects
        Step 13: Search for expected project in response
        Step 14: Compare project names and log results
        Step 15: Verify response structure has 'data' field
        Step 16: Assert expected project was found
        
        Expected Result: Project search API returns projects and finds expected project
        """
        
        # Step 1: Prepare API headers with authentication
        headers = {
            "accept": "*/*",
            "accept-language": "en-GB,en;q=0.9",
            "origin": "https://relay.welocalize.xyz",
            "referer": "https://relay.welocalize.xyz/",
            "x-api-key": "01vsc0FBxm13HfKB8WTtZ2g98i60S6ec5dKpMuR3",
            "x-pantheon-auth": config.AUTH_TOKEN_RELAY
        }
        
        # Step 2: Build full URL with endpoint
        url = f"{self.base_url}{self.endpoint}"
        
        # Step 3: Log request details
        logger.info(f"Request URL: {url}")
        logger.info(f"Query Parameters: {self.query_params}")
        logger.info(f"Headers: {headers}")
        
        # Step 4: Make GET request with query parameters
        response = requests.get(url, params=self.query_params, headers=headers)
        
        # Step 5: Log response details for debugging
        logger.info(f"Response Status: {response.status_code}")
        logger.info(f"Response Headers: {dict(response.headers)}")
        logger.info(f"Response Text: {response.text}")
        logger.info(f"Request URL: {response.url}")
        
        # Step 6: Generate current date for filename
        current_date = datetime.now().strftime("%Y%m%d")
        response_file_path = f"data/api/responses/SearchProject-{current_date}.json"
        
        # Step 7: Create response directory if needed
        os.makedirs(os.path.dirname(response_file_path), exist_ok=True)
        
        # Step 8: Save response data to JSON file
        with open(response_file_path, 'w') as f:
            json.dump(response.json(), f, indent=2)
        
        logger.info(f"Response data saved to: {response_file_path}")
        
        # Step 9: Verify response status code is 200
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.text}"
        
        # Step 10: Verify response is valid JSON object
        response_data = response.json()
        assert isinstance(response_data, dict), "Response should be a JSON object"
        
        # Step 11: Read expected project name from file
        project_name_file = "data/projectname.txt"
        expected_project_name = None
        if os.path.exists(project_name_file):
            with open(project_name_file, 'r') as f:
                expected_project_name = f.read().strip()
            logger.info(f"Expected project name from file: {expected_project_name}")
        else:
            logger.warning("Project name file not found: data/projectname.txt")
        
        # Step 12-13: Parse response data and search for expected project
        if "data" in response_data:
            logger.info(f"Found {len(response_data['data'])} projects in response")
            
            # Check if expected project is found in response
            found_project = False
            found_project_details = None
            
            for i, project in enumerate(response_data['data']):
                project_name = project.get('name', 'N/A')
                project_status = project.get('status', 'N/A')
                billing_ref_id = project.get('billingReferenceId', 'N/A')
                
                logger.info(f"Project {i+1}: {project_name} - Status: {project_status} - BillingRefId: {billing_ref_id}")
                
                # Compare with expected project name
                if expected_project_name and expected_project_name in project_name:
                    found_project = True
                    found_project_details = {
                        'name': project_name,
                        'status': project_status,
                        'billingReferenceId': billing_ref_id,
                        'index': i+1
                    }
                    logger.info(f"✅ MATCH FOUND: Project '{project_name}' matches expected name")
                    logger.info(f"   - Status: {project_status}")
                    logger.info(f"   - Billing Reference ID: {billing_ref_id}")
                    break
            
            # Step 14: Compare project names and log results
            if found_project:
                logger.info(f"✅ Project verification successful!")
                logger.info(f"   Expected: {expected_project_name}")
                logger.info(f"   Found: {found_project_details['name']}")
                logger.info(f"   Billing Reference ID: {found_project_details['billingReferenceId']}")
            else:
                if expected_project_name:
                    logger.warning(f"❌ Project '{expected_project_name}' not found in response")
                    logger.warning("Available projects:")
                    for i, project in enumerate(response_data['data'][:5]):  # Show first 5 projects
                        logger.warning(f"   {i+1}. {project.get('name', 'N/A')}")
                else:
                    logger.info("No expected project name provided for comparison")
        else:
            logger.warning("No 'data' field found in response")
        
        # Step 15: Verify response structure has 'data' field
        assert "data" in response_data, "Response should contain 'data' field"
        assert isinstance(response_data["data"], list), "Data field should be a list"
        
        # Step 16: Assert expected project was found
        if expected_project_name:
            assert found_project, f"Expected project '{expected_project_name}' not found in response"
        
        logger.info("Project search API test completed successfully")
