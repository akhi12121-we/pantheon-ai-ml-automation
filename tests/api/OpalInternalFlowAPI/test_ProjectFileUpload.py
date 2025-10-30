#!/usr/bin/env python3
"""
Test for Opal Internal Flow API - Project File Upload
"""
import pytest
import json
from utils.http_client import APIClient
from utils.data_parser import data_parser
from utils.logger import logger
from config.settings import config


class TestProjectFileUpload:
    """Test class for project file upload API."""
    
    def setup_method(self):
        """Setup method for each test."""
        self.client = APIClient(config.OPAL_FASTAPI_URL)
        
    def test_project_file_upload(self):
        """Test uploading file to project."""
        logger.info("Starting project file upload test")
        
        # Get auth token from data_parser
        auth_token = data_parser.get_opal_token()
        assert auth_token, "Auth token not found"
        
        # Get project ID from the created project response
        project_id = data_parser.get_json_value("api", "response", "opalProjectIdCreated.json", key="id")
        assert project_id, "Project ID not found in response file"
        
        logger.info(f"Using project ID: {project_id}")
        
        # Build endpoint with project ID
        endpoint = f"/internal/v1/projects/{project_id}/files"
        
        # Set authorization header
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        
        # Get file upload data from request file
        file_upload_data = data_parser.get_json_value("api", "requests", "FileUpload.json")
        assert file_upload_data, "File upload data not found in request file"
        
        logger.info(f"File upload data: {file_upload_data}")
        
        # Make POST request
        response = self.client.post(
            endpoint=endpoint,
            data=file_upload_data,
            headers=headers
        )
        
        # Verify response status
        assert response.status_code == 201, f"Expected status 201, got {response.status_code}"
        
        # Parse response
        response_data = response.json()
        logger.info(f"File upload response: {response_data}")
        
        # Save response to file
        data_parser.write_json(
            response_data,
            "api", "response", "FileUploadFileRead.json"
        )
        logger.info(f"File upload response saved to file data/api/response/FileUploadFileRead.json")
        
        # Verify response contains expected fields
        expected_keys = ["id", "name", "type", "source_locale", "target_locale", "project_id", "job_id", "checksum", "upload_url"]
        
        for key in expected_keys:
            assert key in response_data, f"Required key '{key}' not found in response"
            logger.info(f"Key '{key}' exists in response: {response_data.get(key)}")
        
        # Verify uploaded file details match request
        assert response_data["name"] == file_upload_data["name"], f"Expected name '{file_upload_data['name']}', got '{response_data['name']}'"
        assert response_data["type"] == file_upload_data["type"], f"Expected type '{file_upload_data['type']}', got '{response_data['type']}'"
        assert response_data["source_locale"] == file_upload_data["source_locale"], f"Expected source_locale '{file_upload_data['source_locale']}', got '{response_data['source_locale']}'"
        assert response_data["target_locale"] == file_upload_data["target_locale"], f"Expected target_locale '{file_upload_data['target_locale']}', got '{response_data['target_locale']}'"
        
        # Verify project_id matches the one used in request
        assert response_data["project_id"] == int(project_id), f"Expected project_id '{project_id}', got '{response_data['project_id']}'"
        
        # Verify upload_url contains expected pattern
        upload_url = response_data["upload_url"]
        assert upload_url.startswith("https://welo-dev-opal.s3.amazonaws.com/phrase/"), f"Upload URL should start with S3 URL pattern, got: {upload_url}"
        assert f"/phrase/{project_id}/input/" in upload_url, f"Upload URL should contain project path, got: {upload_url}"
        assert "AWSAccessKeyId=" in upload_url, f"Upload URL should contain AWSAccessKeyId, got: {upload_url}"
        
        logger.info("File upload verification passed")
        logger.info("Project file upload test completed successfully")
