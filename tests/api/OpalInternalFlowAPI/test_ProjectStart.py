#!/usr/bin/env python3
"""
Test for Opal Internal Flow API - Project Start
"""
import pytest
import json
from utils.http_client import APIClient
from utils.data_parser import data_parser
from utils.logger import logger
from config.settings import config


class TestProjectStart:
    """Test class for starting project API."""
    
    def setup_method(self):
        """Setup method for each test."""
        self.client = APIClient(config.OPAL_FASTAPI_URL)
        
    def test_project_start(self):
        """Test starting project."""
        logger.info("Starting project start test")
        
        # Get auth token from data_parser
        auth_token = data_parser.get_opal_token()
        assert auth_token, "Auth token not found"
        
        # Get project ID from the created project response
        project_id = data_parser.get_json_value("api", "response", "opalProjectIdCreated.json", key="id")
        assert project_id, "Project ID not found in response file"
        
        logger.info(f"Using project ID: {project_id}")
        
        # Build endpoint with project ID
        endpoint = f"/internal/v1/projects/{project_id}/start"
        
        # Set authorization header
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "accept": "application/json"
        }
        
        # Make POST request
        response = self.client.post(
            endpoint=endpoint,
            headers=headers
        )
        
        # Verify response status
        assert response.status_code == 204, f"Expected status 204, got {response.status_code}"
        
        logger.info("Project start test completed successfully")
