"""
Test cases for XTM Pull Project Scheduler API.
"""
import pytest
import json
import os
import datetime
from utils.http_client import APIClient
from utils.auth_helper import AuthHelper
from config.settings import config
from utils.logger import logger


class TestPullProjectScheduler:
    """Test class for XTM Pull Project Scheduler API."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test fixtures."""
        self.base_url = config.PULL_PROJECT_API_URL
        self.auth_token = config.AUTH_TOKEN_PANTHEON
        self.endpoint = "/api/jobs/platform-get-projects"
        
        # Load test data
        test_data_path = os.path.join(config.API_REQUESTS_PATH, "pullProjectXTM.json")
        with open(test_data_path, 'r') as f:
            self.test_data = json.load(f)
    
    @pytest.mark.projectcreation
    def test_02_pull_project_trigger_job(self):
        """
        Test triggering XTM pull project job.
        
        TEST WORKFLOW STEPS:
        ===================
        Step 1: Setup authentication with Pantheon token
        Step 2: Initialize API client with base URL and auth
        Step 3: Prepare request payload with test data
        Step 4: Make POST request to pull project endpoint
        Step 5: Verify response status code is 200
        Step 6: Verify response is valid JSON object
        Step 7: Log response status and data for debugging
        Step 8: Generate unique timestamp for filename
        Step 9: Save response data to JSON file
        Step 10: Log file save location
        
        Expected Result: XTM pull project job triggered successfully
        """
        # Step 1-2: Setup authentication and API client
        auth = AuthHelper(self.auth_token)
        client = APIClient(self.base_url, auth)
        
        # Step 3: Prepare request payload
        payload = {"payload": self.test_data}
        
        # Step 4: Make POST request
        response = client.post(self.endpoint, data=payload)
        
        # Step 5: Verify response status code
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
        
        # Step 6: Verify response is JSON
        response_data = response.json()
        assert isinstance(response_data, dict), "Response should be a JSON object"
        
        # Step 7: Log response for debugging
        logger.info(f"Response Status: {response.status_code}")
        logger.info(f"Response Data: {response_data}")
    
        # Step 8: Generate unique timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        response_filename = f"unique_filename_{timestamp}_XTMPullResponse.json"
        response_file_path = os.path.join(config.API_RESPONSES_PATH, response_filename)
        
        # Step 9: Save response to file
        with open(response_file_path, 'w') as f:
            json.dump(response_data, f, indent=2)
        
        # Step 10: Log file save location
        logger.info(f"Response saved to: {response_file_path}")