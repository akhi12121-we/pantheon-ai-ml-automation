"""
Test to verify generated Opal token is valid
"""
import pytest
from utils.http_client import APIClient
from utils.logger import logger
from utils.data_parser import data_parser
from config.settings import config


class TestVerifyGeneratedToken:
    """Test class for verifying generated Opal token."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test fixtures."""
        self.base_url = config.OPAL_FASTAPI_URL
        self.client = APIClient(self.base_url)
    
    def test_verify_generated_token(self):
        """Test to verify the generated token is valid."""
        logger.info("Starting token verification test")
        
        # Get the saved auth token
        auth_token = data_parser.get_opal_token()
        assert auth_token, "No auth token found. Run token generation test first."
        
        logger.info(f"Retrieved auth token: {auth_token[:20]}...")
        
        # API endpoint with token parameter
        endpoint = f"/internal/v1/auth/token/info?token={auth_token}"
        
        # Headers using http_client utility
        headers = {
            "X-API-KEY": config.AUTH_CLIENT_TOKEN_OPAL,
            "accept": "application/json"
        }
        
        logger.info(f"Making GET request to {self.base_url}{endpoint}")
        
        # Make the API request using http_client
        response = self.client.get(endpoint, headers=headers)
        
        logger.info(f"Response status code: {response.status_code}")
        logger.info(f"Response data: {response.json()}")
        
        # Parse response
        response_data = response.json()
        
        # Simple assertions - only version and empty scope
        assert response_data["version"] == 1
        logger.info(f"Expected version 1, got {response_data['version']}")
        assert response_data["scope"] == {}
        logger.info(f"Expected empty scope, got {response_data['scope']}")
        
        logger.info("Token verification test completed successfully")
