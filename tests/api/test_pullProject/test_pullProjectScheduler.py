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
        """Test triggering XTM pull project job."""
        # Setup authentication
        auth = AuthHelper(self.auth_token)
        client = APIClient(self.base_url, auth)
        
        # Prepare request payload
        payload = {"payload": self.test_data}
        
        # Make POST request
        response = client.post(self.endpoint, data=payload)
        
        # Assertions
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
        
        # Verify response is JSON
        response_data = response.json()
        assert isinstance(response_data, dict), "Response should be a JSON object"
        
        # Log response for debugging
        logger.info(f"Response Status: {response.status_code}")
        logger.info(f"Response Data: {response_data}")
    
        
        # Save response to file
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        response_filename = f"unique_filename_{timestamp}_XTMPullResponse.json"
        response_file_path = os.path.join(config.API_RESPONSES_PATH, response_filename)
        
        with open(response_file_path, 'w') as f:
            json.dump(response_data, f, indent=2)
        
        logger.info(f"Response saved to: {response_file_path}")