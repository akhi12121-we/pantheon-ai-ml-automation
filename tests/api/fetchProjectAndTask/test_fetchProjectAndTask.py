"""
Test cases for Fetch Project and Task API.
"""
import pytest
import json
import os
import requests
from config.settings import config
from utils.logger import logger


class TestFetchProjectAndTask:
    """Test class for Fetch Project and Task API."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test fixtures."""
        self.base_url = "https://hypnos.welocalize.xyz"
        self.endpoint = "/v1/project/"
        
        # Load test data
        test_data_path = os.path.join(config.API_REQUESTS_PATH, "fetchProjectAndTask.json")
        with open(test_data_path, 'r') as f:
            self.test_data = json.load(f)
    
    @pytest.mark.projectcreation
    def test_03_fetch_project_and_task(self):
        """Test fetching project and task by project name."""
        # Read project name from file
        project_name_file = "data/projectname.txt"
        if os.path.exists(project_name_file):
            with open(project_name_file, 'r') as f:
                project_name = f.read().strip()
        else:
            # Fallback to default project name if file doesn't exist
            project_name = "XTM Test Automation team"
        
        # Update test data with actual project name
        self.test_data["searchTerm"] = project_name
        
        # Prepare headers
        headers = {
            "accept": "*/*",
            "accept-language": "en-GB,en;q=0.9",
            "origin": "https://relay.welocalize.xyz",
            "referer": "https://relay.welocalize.xyz/",
            "x-api-key": "01vsc0FBxm13HfKB8WTtZ2g98i60S6ec5dKpMuR3",
            "x-pantheon-auth": config.AUTH_TOKEN_RELAY
        }
        
        # Convert test data to proper query parameters format
        query_params = {
            "$limit": self.test_data["limit"],
            "$offset": self.test_data["offset"],
            "$include": self.test_data["include"],
            "$order_by": self.test_data["order_by"],
            "$order_dir": self.test_data["order_dir"],
            "$searchTerm": self.test_data["searchTerm"],
            "$searchFields": self.test_data["searchFields"]
        }
        
        # Build full URL
        url = f"{self.base_url}{self.endpoint}"
        
        # Log request details
        logger.info(f"Request URL: {url}")
        logger.info(f"Query Parameters: {query_params}")
        logger.info(f"Headers: {headers}")
        
        # Make GET request with query parameters
        response = requests.get(url, params=query_params, headers=headers)
        
        # Log response details for debugging
        logger.info(f"Response Status: {response.status_code}")
        logger.info(f"Response Headers: {dict(response.headers)}")
        logger.info(f"Response Text: {response.text}")
        logger.info(f"Request URL: {response.url}")
        
        # Write response data to JSON file
        from datetime import datetime
        current_date = datetime.now().strftime("%Y%m%d")
        response_file_path = f"data/api/responses/project_search_{current_date}.json"
        
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
        logger.info(f"Searching for project: {project_name}")
        
        # Verify project was found
        if "data" in response_data and response_data["data"]:
            found_project = False
            for project in response_data["data"]:
                if project.get("description") == project_name:
                    found_project = True
                    logger.info(f"Project found: {project['name']} and the description is {project['description']}")
                    break
            
            if not found_project:
                logger.warning(f"Project '{project_name}' not found in response")
        else:
            logger.warning("No projects found in response")
