#!/usr/bin/env python3
"""
Test for Opal Internal Flow API - Get Project Details After Complete
"""
import pytest
import json
from utils.http_client import APIClient
from utils.data_parser import data_parser
from utils.logger import logger
from config.settings import config


class TestGetProjectDetailsAfterComplete:
    """Test class for getting project details API after completion."""
    
    def setup_method(self):
        """Setup method for each test."""
        self.client = APIClient(config.OPAL_FASTAPI_URL)
        
    def test_get_project_details_after_complete(self):
        """Test getting project details by ID after completion."""
        logger.info("Starting get project details after complete test")
        
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
        
        # Get expected values from the created project response
        expected_orchestrator_project_id = data_parser.get_json_value("api", "response", "opalProjectIdCreated.json", key="orchestrator_project_id")
        expected_domain_id = data_parser.get_json_value("api", "response", "opalProjectIdCreated.json", key="domain_id")
        expected_client_id = data_parser.get_json_value("api", "response", "opalProjectIdCreated.json", key="client_id")
        expected_callback_url = data_parser.get_json_value("api", "response", "opalProjectIdCreated.json", key="callback_url")
        expected_customer_id = data_parser.get_json_value("api", "response", "opalProjectIdCreated.json", key="customer_id")
        expected_orchestrator = data_parser.get_json_value("api", "response", "opalProjectIdCreated.json", key="orchestrator")
        
        # Verify orchestrator_project_id matches
        assert response_data["orchestrator_project_id"] == expected_orchestrator_project_id, f"Expected orchestrator_project_id '{expected_orchestrator_project_id}', got '{response_data['orchestrator_project_id']}'"
        logger.info(f"Orchestrator project ID verification passed: {response_data['orchestrator_project_id']}")
        
        # Verify domain_id matches
        assert response_data["domain_id"] == expected_domain_id, f"Expected domain_id '{expected_domain_id}', got '{response_data['domain_id']}'"
        logger.info(f"Domain ID verification passed: {response_data['domain_id']}")
        
        # Verify client_id matches
        assert response_data["client_id"] == expected_client_id, f"Expected client_id '{expected_client_id}', got '{response_data['client_id']}'"
        logger.info(f"Client ID verification passed: {response_data['client_id']}")
        
        # Verify callback_url matches
        assert response_data["callback_url"] == expected_callback_url, f"Expected callback_url '{expected_callback_url}', got '{response_data['callback_url']}'"
        logger.info(f"Callback URL verification passed: {response_data['callback_url']}")
        
        # Verify customer_id matches
        assert response_data["customer_id"] == expected_customer_id, f"Expected customer_id '{expected_customer_id}', got '{response_data['customer_id']}'"
        logger.info(f"Customer ID verification passed: {response_data['customer_id']}")
        
        # Verify orchestrator matches
        assert response_data["orchestrator"] == expected_orchestrator, f"Expected orchestrator '{expected_orchestrator}', got '{response_data['orchestrator']}'"
        logger.info(f"Orchestrator verification passed: {response_data['orchestrator']}")
        
        # Verify status is finished
        assert response_data["status"] == "finished", f"Expected status 'finished', got '{response_data['status']}'"
        logger.info(f"Status verification passed: {response_data['status']}")
        
        # Verify files array has exactly 2 items (input and final files)
        assert len(response_data["files"]) == 2, f"Expected files array to have exactly 2 items, got {len(response_data['files'])}"
        logger.info(f"Files array verification passed: {len(response_data['files'])} files found")
        
        logger.info("Get project details after complete test completed successfully")
