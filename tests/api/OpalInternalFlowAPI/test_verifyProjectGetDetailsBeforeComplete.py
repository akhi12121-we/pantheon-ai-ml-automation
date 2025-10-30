#!/usr/bin/env python3
"""
Test for Opal Internal Flow API - Get Project Details
"""
import pytest
import json
from utils.http_client import APIClient
from utils.data_parser import data_parser
from utils.logger import logger
from config.settings import config


class TestGetProjectDetails:
    """Test class for getting project details API."""
    
    def setup_method(self):
        """Setup method for each test."""
        self.client = APIClient(config.OPAL_FASTAPI_URL)
        
    def test_get_project_details(self):
        """Test getting project details by ID."""
        logger.info("Starting get project details test")
        
        # Get auth token from data_parser
        auth_token = data_parser.get_opal_token()
        assert auth_token, "Auth token not found"
        
        # Get project ID from the created project response
        project_id = data_parser.get_json_value("api", "response", "opalProjectIdCreated.json", key="id")
        assert project_id, "Project ID not found in response file"
        
        logger.info(f"Using project ID: {project_id}")
        
        # Build endpoint with project ID
        endpoint = f"/internal/v1/projects/{project_id}"
        
        # Set authorization header
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "accept": "application/json"
        }
        
        # Make GET request
        response = self.client.get(
            endpoint=endpoint,
            headers=headers
        )
        
        # Verify response status
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
        
        # Parse response
        response_data = response.json()
        logger.info(f"Project details response: {response_data}")
        
        # Verify all keys exist in response
        expected_keys = [
            "orchestrator_project_id",
            "domain_id", 
            "buyer_id",
            "client_id",
            "callback_url",
            "id",
            "customer_id",
            "orchestrator",
            "status",
            "fail_reason",
            "completed_at",
            "expires_at",
            "files"
        ]
        
        for key in expected_keys:
            assert key in response_data, f"Required key '{key}' not found in response"
            logger.info(f"Key '{key}' exists in response: {response_data.get(key)}")
        
        # Get expected customer_id from the created project response
        expected_customer_id = data_parser.get_json_value("api", "response", "opalProjectIdCreated.json", key="customer_id")
        logger.info(f"Expected customer_id from file: {expected_customer_id}")
        
        # Verify customer_id matches the one from created project
        assert response_data["customer_id"] == expected_customer_id, f"Expected customer_id '{expected_customer_id}', got '{response_data['customer_id']}'"
        logger.info(f"Customer ID verification passed: {response_data['customer_id']}")
        
        # Verify orchestrator
        assert response_data["orchestrator"] == "phrase", f"Expected orchestrator 'phrase', got '{response_data['orchestrator']}'"
        logger.info(f"Orchestrator verification passed: {response_data['orchestrator']}")
        
        # Verify status
        assert response_data["status"] == "created", f"Expected status 'created', got '{response_data['status']}'"
        logger.info(f"Status verification passed: {response_data['status']}")
        
        logger.info("Get project details test completed successfully")