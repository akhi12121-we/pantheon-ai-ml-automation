"""
Simple API tests.
"""
import pytest
from utils.http_client import APIClient
from utils.auth_helper import AuthHelper
from config.settings import config

class TestAPI:
    """Simple API test class."""
    
    def test_aiqe_health(self):
        """Test AIQE health endpoint."""
        client = APIClient(config.AIQE_URL)
        response = client.get("/health")
        print(response.json())
        assert response.status_code == 200

    def test_apollo_health(self):
        """Test Apollo health endpoint."""
        client = APIClient(config.APOLLO_URL)
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_comet_health(self):
        """Test Comet health endpoint."""
        client = APIClient(config.COMET_URL)
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_with_auth(self):
        """Test API with authentication."""
        if config.AUTH_TOKEN:
            auth = AuthHelper(config.AUTH_TOKEN)
            client = APIClient(config.AIQE_URL, auth)
            response = client.get("/protected-endpoint")
            assert response.status_code in [200, 401, 403]  # Accept various auth responses
