#!/usr/bin/env python3
"""
Test for Opal Internal Flow API - Project Multi File Upload
"""
import pytest
import json
from utils.http_client import APIClient
from utils.data_parser import data_parser
from utils.logger import logger
from config.settings import config


class TestProjectMultiFileUpload:
    """Test class for project multi file upload API."""
    
    def setup_method(self):
        """Setup method for each test."""
        self.client = APIClient(config.OPAL_FASTAPI_URL)
        
    def test_project_file_multiupload(self):
        """Test re-uploading file to project."""
        logger.info("Starting project multi file upload test")
        
        # Get auth token from data_parser
        auth_token = data_parser.get_opal_token()
        assert auth_token, "Auth token not found"
        
        # Get project ID from the created project response
        project_id = data_parser.get_json_value("api", "response", "opalProjectIdCreated.json", key="id")
        assert project_id, "Project ID not found in response file"
        
        # Get file ID from the file upload response
        file_id = data_parser.get_json_value("api", "response", "FileUploadFileRead.json", key="id")
        assert file_id, "File ID not found in response file"
        
        logger.info(f"Using project ID: {project_id}")
        logger.info(f"Using file ID: {file_id}")
        
        # Build endpoint with project ID and file ID
        endpoint = f"/internal/v1/projects/{project_id}/files/{file_id}/re-upload"
        
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
        logger.info(f"Multi file upload response: {response_data}")
        
        # Verify response contains expected fields
        expected_keys = ["id", "name", "type", "source_locale", "target_locale", "project_id", "job_id", "checksum", "upload_url"]
        
        for key in expected_keys:
            assert key in response_data, f"Required key '{key}' not found in response"
            logger.info(f"Key '{key}' exists in response: {response_data.get(key)}")
        
        # Verify project_id matches the one used in request
        assert response_data["project_id"] == int(project_id), f"Expected project_id '{project_id}', got '{response_data['project_id']}'"
        
        # Verify upload_url contains expected pattern
        upload_url = response_data["upload_url"]
        assert upload_url.startswith("https://welo-dev-opal.s3.amazonaws.com/phrase/"), f"Upload URL should start with S3 URL pattern, got: {upload_url}"
        assert f"/phrase/{project_id}/input/" in upload_url, f"Upload URL should contain project path, got: {upload_url}"
        assert "AWSAccessKeyId=" in upload_url, f"Upload URL should contain AWSAccessKeyId, got: {upload_url}"
        
        logger.info("Multi file upload verification passed")
        logger.info("Project multi file upload test completed successfully")
