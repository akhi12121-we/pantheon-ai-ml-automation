#!/usr/bin/env python3
"""
Test for Opal Internal Flow API - Project Complete
"""
import pytest
import json
from utils.http_client import APIClient
from utils.data_parser import data_parser
from utils.logger import logger
from config.settings import config


class TestProjectComplete:
    """Test class for completing project API."""
    
    def setup_method(self):
        """Setup method for each test."""
        self.client = APIClient(config.OPAL_FASTAPI_URL)
        
    def test_project_complete(self):
        """Test completing project."""
        logger.info("Starting project complete test")
        
        # Get auth token from data_parser
        auth_token = data_parser.get_opal_token()
        assert auth_token, "Auth token not found"
        
        # Get project ID from the created project response
        project_id = data_parser.get_json_value("api", "response", "opalProjectIdCreated.json", key="id")
        assert project_id, "Project ID not found in response file"
        
        logger.info(f"Using project ID: {project_id}")
        
        # Build endpoint with project ID
        endpoint = f"/internal/v1/projects/{project_id}/complete"
        
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
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
        
        # Parse response
        response_data = response.json()
        logger.info(f"Project complete response: {response_data}")
        
        # Verify response is a list
        assert isinstance(response_data, list), f"Expected list response, got {type(response_data)}"
        assert len(response_data) > 0, "Response list should not be empty"
        
        # Get first item from response list
        first_item = response_data[0]
        
        # Verify response contains expected fields
        expected_keys = ["id", "name", "type", "source_locale", "target_locale", "project_id", "job_id", "checksum", "upload_url"]
        
        for key in expected_keys:
            assert key in first_item, f"Required key '{key}' not found in response"
            logger.info(f"Key '{key}' exists in response: {first_item.get(key)}")
        
        # Verify project_id matches the one used in request
        assert first_item["project_id"] == int(project_id), f"Expected project_id '{project_id}', got '{first_item['project_id']}'"
        
        # Verify upload_url contains expected pattern
        upload_url = first_item["upload_url"]
        assert upload_url.startswith("https://welo-dev-opal.s3.amazonaws.com/phrase/"), f"Upload URL should start with S3 URL pattern, got: {upload_url}"
        assert f"/phrase/{project_id}/final/" in upload_url, f"Upload URL should contain project path with final, got: {upload_url}"
        assert "AWSAccessKeyId=" in upload_url, f"Upload URL should contain AWSAccessKeyId, got: {upload_url}"
        
        logger.info("Project complete verification passed")
        logger.info("Project complete test completed successfully")
