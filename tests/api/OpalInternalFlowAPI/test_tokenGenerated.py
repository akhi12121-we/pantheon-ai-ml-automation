"""
Opal Internal Flow API Token Generation Tests
"""
import pytest
import json
import os
from utils.http_client import APIClient
from utils.logger import logger
from utils.data_parser import data_parser
from config.settings import config


class TestOpalTokenGeneration:
    """Test class for Opal token generation API."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test fixtures."""
        self.base_url = config.OPAL_FASTAPI_URL
        self.client = APIClient(self.base_url)
        self.response_file = "data/api/response/opaltokenGeneration.json"
    
    def test_generate_token(self):
        """Test token generation API."""
        logger.info("Starting Opal token generation test")
        
        # Generate dynamic name
        dynamic_name = APIClient.generate_dynamic_name()
        logger.info(f"Generated dynamic name: {dynamic_name}")
        
        # Load request payload from JSON file
        payload = data_parser.read_json("api", "requests", "opalTokenGenerationReq.json")
        assert payload, "Failed to load request payload from JSON file"
        
        # Update payload with dynamic values
        payload["customer_id"] = dynamic_name
        payload["created_by_email"] = f"{dynamic_name}@gmail.com"
        
        # API endpoint
        endpoint = "/internal/v1/auth/token"
        
        # Headers using http_client utility
        headers = {
            "X-API-KEY": config.AUTH_CLIENT_TOKEN_OPAL,
            "accept": "application/json"
        }
        
        logger.info(f"Making POST request to {self.base_url}{endpoint}")
        logger.info(f"Request payload: {payload}")
        
        try:
            # Make the API request
            response = self.client.post(endpoint, data=payload, headers=headers)
            
            logger.info(f"Response status code: {response.status_code}")
            logger.info(f"Response headers: {dict(response.headers)}")
            
            # Check if request was successful
            assert response.status_code == 201, f"Expected status 201, got {response.status_code}"
            
            # Parse response
            response_data = response.json()
            logger.info(f"Response data: {response_data}")
            
            # Validate response structure
            assert "auth_token" in response_data, "Response missing auth_token"
            assert "refresh_token" in response_data, "Response missing refresh_token"
            assert "auth_token_expires_at" in response_data, "Response missing auth_token_expires_at"
            
            # Save response to file
            self._save_response(response_data)
            
            logger.info("Token generation test completed successfully")
            
        except Exception as e:
            logger.error(f"Token generation test failed: {str(e)}")
            raise
    
    def _save_response(self, response_data):
        """Save response data to JSON file."""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.response_file), exist_ok=True)
            
            # Save response to file
            with open(self.response_file, 'w', encoding='utf-8') as f:
                json.dump(response_data, f, indent=2)
            
            logger.info(f"Response saved to {self.response_file}")
            
        except Exception as e:
            logger.error(f"Failed to save response: {str(e)}")
            raise
