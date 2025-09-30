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
        """Test fetching projects using platform-project API."""
        
        # Prepare headers
        headers = {
            "accept": "*/*",
            "accept-language": "en-GB,en;q=0.9",
            "origin": "https://relay.welocalize.xyz",
            "referer": "https://relay.welocalize.xyz/",
            "x-api-key": "01vsc0FBxm13HfKB8WTtZ2g98i60S6ec5dKpMuR3",
            "x-pantheon-auth": config.AUTH_TOKEN_RELAY
        }
        
        # Build full URL
        url = f"{self.base_url}{self.endpoint}"
        
        # Log request details
        logger.info(f"Request URL: {url}")
        logger.info(f"Query Parameters: {self.query_params}")
        logger.info(f"Headers: {headers}")
        
        # Make GET request with query parameters
        response = requests.get(url, params=self.query_params, headers=headers)
        
        # Log response details for debugging
        logger.info(f"Response Status: {response.status_code}")
        logger.info(f"Response Headers: {dict(response.headers)}")
        logger.info(f"Response Text: {response.text}")
        logger.info(f"Request URL: {response.url}")
        
        # Save response to file with current date
        current_date = datetime.now().strftime("%Y%m%d")
        response_file_path = f"data/api/responses/SearchProject-{current_date}.json"
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(response_file_path), exist_ok=True)
        
        # Write response data to file
        with open(response_file_path, 'w') as f:
            json.dump(response.json(), f, indent=2)
        
        logger.info(f"Response data saved to: {response_file_path}")
        
        # Assertions
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.text}"
        
        # Verify response is JSON
        response_data = response.json()
        assert isinstance(response_data, dict), "Response should be a JSON object"
        
        # Log response for debugging
        logger.info(f"Response Status: {response.status_code}")
        logger.info(f"Response Data: {response_data}")
        
        # Read project name from file for comparison
        project_name_file = "data/projectname.txt"
        expected_project_name = None
        if os.path.exists(project_name_file):
            with open(project_name_file, 'r') as f:
                expected_project_name = f.read().strip()
            logger.info(f"Expected project name from file: {expected_project_name}")
        else:
            logger.warning("Project name file not found: data/projectname.txt")
        
        # Verify response structure and compare with expected project
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
            
            # Log comparison results
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
        
        # Verify response has expected structure
        assert "data" in response_data, "Response should contain 'data' field"
        assert isinstance(response_data["data"], list), "Data field should be a list"
        
        # If we have an expected project name, verify it was found
        if expected_project_name:
            assert found_project, f"Expected project '{expected_project_name}' not found in response"
        
        logger.info("Project search API test completed successfully")
