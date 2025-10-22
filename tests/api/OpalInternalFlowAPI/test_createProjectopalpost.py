#!/usr/bin/env python3
"""
Test for Opal Internal Flow API - Project Creation
"""
import pytest
import json
from utils.http_client import APIClient
from utils.data_parser import data_parser
from utils.logger import logger
from config.settings import config


class TestCreateProject:
    """Test class for project creation API."""
    
    def setup_method(self):
        """Setup method for each test."""
        self.client = APIClient(config.OPAL_FASTAPI_URL)
        self.endpoint = "/internal/v1/projects"
        
        
    def test_create_project(self):
        """Test project creation API."""
        logger.info("Starting project creation test")
        
        # Get auth token from data_parser
        auth_token = data_parser.get_opal_token()
        assert auth_token, "Auth token not found"
        
        # Prepare request data
        request_data = data_parser.read_json("api", "requests", "opalProjectCreation.json")
        assert request_data, "Failed to load request payload from JSON file"
        
        # Generate dynamic name and update fields
        dynamic_name_orchestrator_project_id = APIClient.generate_dynamic_name()
        dynamic_name_domain_id = APIClient.generate_dynamic_smallnum("domain")
        dynamic_name_buyer_id = APIClient.generate_dynamic_smallnum("buyer")
        dynamic_name_client_id = APIClient.generate_dynamic_smallnum("client")
        request_data["orchestrator_project_id"] = dynamic_name_orchestrator_project_id
        request_data["domain_id"] = dynamic_name_domain_id
        request_data["buyer_id"] = dynamic_name_buyer_id
        request_data["client_id"] = dynamic_name_client_id
        # request_data["customer_id"] = f"Automation_{dynamic_name}testRecord{dynamic_name}"
        
        logger.info(f"Request data: {request_data}")
        
        # Set authorization header
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        
        # Make POST request
        response = self.client.post(
            endpoint=self.endpoint,
            data=request_data,
            headers=headers
        )
        
        # Verify response status
        assert response.status_code == 201, f"Expected status 201, got {response.status_code}"
        
        # Parse response
        response_data = response.json()
        logger.info(f"Project creation response: {response_data}")
        
        # Save response to file
        data_parser.write_json(
            response_data,
            "api", "response", "opalProjectIdCreated.json"
        )
        
        # Verify required keys exist
        required_keys = [
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
            "expires_at"
        ]
        
        for key in required_keys:
            assert key in response_data, f"Required key '{key}' not found in response"
        
        # Verify specific values
        assert response_data["orchestrator"] == "phrase", f"Expected orchestrator 'phrase', got '{response_data['orchestrator']}'"
        logger.info(f"Expected orchestrator 'phrase', got '{response_data['orchestrator']}'")
        assert response_data["status"] == "created", f"Expected status 'created', got '{response_data['status']}'"
        logger.info(f"Expected status 'created', got '{response_data['status']}'")
        # Verify input data matches response
        assert response_data["orchestrator_project_id"] == request_data["orchestrator_project_id"]
        logger.info(f"Expected orchestrator project id '{request_data['orchestrator_project_id']}', got '{response_data['orchestrator_project_id']}'")
        assert response_data["domain_id"] == request_data["domain_id"]
        logger.info(f"Expected domain id '{request_data['domain_id']}', got '{response_data['domain_id']}'")
        assert response_data["buyer_id"] == request_data["buyer_id"]
        logger.info(f"Expected buyer id '{request_data['buyer_id']}', got '{response_data['buyer_id']}'")
        assert response_data["client_id"] == request_data["client_id"]
        logger.info(f"Expected client id '{request_data['client_id']}', got '{response_data['client_id']}'")
        assert response_data["callback_url"] == request_data["callback_url"]
        logger.info(f"Expected callback url '{request_data['callback_url']}', got '{response_data['callback_url']}'")
        # Verify generated fields
        assert response_data["id"] is not None, "Project ID should not be null"
        logger.info(f"Expected project id '{response_data['id']}', got '{response_data['id']}'")
        assert response_data["customer_id"] is not None, "Customer ID should not be null"
        logger.info(f"Expected customer id '{response_data['customer_id']}', got '{response_data['customer_id']}'")
        assert response_data["expires_at"] is not None, "Expires at should not be null"
        logger.info(f"Expected expires at '{response_data['expires_at']}', got '{response_data['expires_at']}'")
        
        logger.info("Project creation test completed successfully")
