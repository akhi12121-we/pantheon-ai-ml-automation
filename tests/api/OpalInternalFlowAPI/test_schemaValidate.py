"""
Opal Internal Flow API Schema Validation Tests
"""
import json
import os
import pytest
from utils.logger import logger
from utils.allure_helper import allure_helper


class TestOpalInternalFlowAPISchema:
    """Test class for Opal Internal Flow API schema validation."""
    
    @pytest.fixture
    def load_schema(self):
        """Load the OpenAPI schema from file."""
        schema_path = os.path.join(
            os.path.dirname(__file__), 
            '../../../data/api/schemas/opal_internal_flow_api.json'
        )
        
        try:
            with open(schema_path, 'r', encoding='utf-8') as schema_file:
                schema = json.load(schema_file)
            logger.info(f"Successfully loaded schema from {schema_path}")
            return schema
        except FileNotFoundError:
            pytest.fail(f"Schema file not found at {schema_path}")
        except json.JSONDecodeError as e:
            pytest.fail(f"Invalid JSON in schema file: {e}")
    
    def test_openapi_schema_structure(self, load_schema):
        """Test that the OpenAPI schema has the required structure."""
        logger.info("Starting OpenAPI schema structure validation")
        schema = load_schema
        
        # Validate required OpenAPI fields
        logger.info("Validating required OpenAPI fields")
        assert "openapi" in schema, "Schema missing 'openapi' field"
        assert "info" in schema, "Schema missing 'info' field"
        assert "paths" in schema, "Schema missing 'paths' field"
        assert "components" in schema, "Schema missing 'components' field"
        
        # Validate OpenAPI version
        logger.info(f"Validating OpenAPI version: {schema['openapi']}")
        assert schema["openapi"].startswith("3."), f"Unsupported OpenAPI version: {schema['openapi']}"
        
        # Validate info section
        logger.info("Validating info section")
        info = schema["info"]
        assert "title" in info, "Schema info missing 'title'"
        assert "version" in info, "Schema info missing 'version'"
        assert info["title"] == "Internal Opal API", f"Unexpected API title: {info['title']}"
        
        logger.info("OpenAPI schema structure validation passed")
    
    def test_api_endpoints_exist(self, load_schema):
        """Test that expected API endpoints are present."""
        logger.info("Starting API endpoints validation")
        schema = load_schema
        paths = schema.get("paths", {})
        
        # Expected endpoints based on the schema
        expected_endpoints = [
            "/v1/auth/token",
            "/v1/auth/token/refresh", 
            "/v1/auth/token/revoke",
            "/v1/auth/token/info",
            "/v1/projects",
            "/v1/projects/{project_id}",
            "/v1/projects/{project_id}/cancel",
            "/v1/projects/{project_id}/complete",
            "/v1/projects/{project_id}/files",
            "/v1/projects/{project_id}/start",
            "/v1/projects/{project_id}/files/{file_id}/re-upload"
        ]
        
        logger.info(f"Checking {len(expected_endpoints)} expected endpoints")
        for endpoint in expected_endpoints:
            logger.info(f"Validating endpoint: {endpoint}")
            assert endpoint in paths, f"Expected endpoint '{endpoint}' not found in schema"
        
        logger.info(f"All {len(expected_endpoints)} expected endpoints found in schema")
    
    def test_schema_components(self, load_schema):
        """Test that schema components are properly defined."""
        logger.info("Starting schema components validation")
        schema = load_schema
        components = schema.get("components", {})
        
        # Check for schemas section
        logger.info("Validating schemas section")
        assert "schemas" in components, "Schema missing 'components.schemas'"
        schemas = components["schemas"]
        
        # Check for key schema definitions
        expected_schemas = [
            "TokenCreateRequest",
            "TokenResponse", 
            "TokenRefreshRequest",
            "TokenRefreshResponse",
            "TokenRevokeRequest",
            "TokenInfoResponse",
            "ProjectCreateRequest",
            "ProjectResponse",
            "ProjectDetailsWithFilesResponse",
            "ProjectFileCreateRequest",
            "UploadFileResponse",
            "DownloadFileResponse",
            "ErrorResponse",
            "ProjectStatus"
        ]
        
        logger.info(f"Validating {len(expected_schemas)} expected schemas")
        for schema_name in expected_schemas:
            logger.info(f"Checking schema: {schema_name}")
            assert schema_name in schemas, f"Expected schema '{schema_name}' not found"
        
        # Check for security schemes
        logger.info("Validating security schemes")
        assert "securitySchemes" in components, "Schema missing 'components.securitySchemes'"
        security_schemes = components["securitySchemes"]
        assert "APIKeyHeader" in security_schemes, "Missing APIKeyHeader security scheme"
        assert "HTTPBearer" in security_schemes, "Missing HTTPBearer security scheme"
        
        logger.info(f"All {len(expected_schemas)} expected schemas found")
    
    def test_authentication_endpoints(self, load_schema):
        """Test authentication endpoints have proper structure."""
        logger.info("Starting authentication endpoints validation")
        schema = load_schema
        paths = schema.get("paths", {})
        
        # Test token creation endpoint
        logger.info("Validating token creation endpoint")
        token_endpoint = paths.get("/v1/auth/token", {})
        assert "post" in token_endpoint, "Token creation endpoint missing POST method"
        
        post_method = token_endpoint["post"]
        assert "requestBody" in post_method, "Token creation missing request body"
        assert "responses" in post_method, "Token creation missing responses"
        assert "201" in post_method["responses"], "Token creation missing 201 response"
        
        # Test token refresh endpoint
        logger.info("Validating token refresh endpoint")
        refresh_endpoint = paths.get("/v1/auth/token/refresh", {})
        assert "post" in refresh_endpoint, "Token refresh endpoint missing POST method"
        
        # Test token info endpoint
        logger.info("Validating token info endpoint")
        info_endpoint = paths.get("/v1/auth/token/info", {})
        assert "get" in info_endpoint, "Token info endpoint missing GET method"
        
        logger.info("Authentication endpoints validation passed")
    
    def test_project_endpoints(self, load_schema):
        """Test project management endpoints have proper structure."""
        logger.info("Starting project endpoints validation")
        schema = load_schema
        paths = schema.get("paths", {})
        
        # Test project creation endpoint
        logger.info("Validating project creation endpoint")
        projects_endpoint = paths.get("/v1/projects", {})
        assert "post" in projects_endpoint, "Projects endpoint missing POST method"
        
        # Test project details endpoint
        logger.info("Validating project details endpoint")
        project_details_endpoint = paths.get("/v1/projects/{project_id}", {})
        assert "get" in project_details_endpoint, "Project details endpoint missing GET method"
        
        # Test project operations endpoints
        project_operations = [
            "/v1/projects/{project_id}/cancel",
            "/v1/projects/{project_id}/complete", 
            "/v1/projects/{project_id}/start"
        ]
        
        logger.info(f"Validating {len(project_operations)} project operation endpoints")
        for operation in project_operations:
            logger.info(f"Checking project operation: {operation}")
            endpoint = paths.get(operation, {})
            assert "post" in endpoint, f"Project operation '{operation}' missing POST method"
        
        logger.info("Project endpoints validation passed")
    
    def test_schema_json_validity(self, load_schema):
        """Test that the schema is valid JSON and has proper structure."""
        logger.info("Starting schema JSON validity validation")
        schema = load_schema
        
        # Test that it's a dictionary (valid JSON object)
        logger.info("Validating JSON object structure")
        assert isinstance(schema, dict), "Schema is not a valid JSON object"
        
        # Test that required top-level keys exist and are correct types
        logger.info("Validating top-level keys and types")
        assert isinstance(schema.get("openapi"), str), "OpenAPI version should be string"
        assert isinstance(schema.get("info"), dict), "Info should be object"
        assert isinstance(schema.get("paths"), dict), "Paths should be object"
        assert isinstance(schema.get("components"), dict), "Components should be object"
        
        # Test that paths contain valid endpoint definitions
        logger.info("Validating paths and HTTP methods")
        paths = schema.get("paths", {})
        for path, methods in paths.items():
            logger.info(f"Validating path: {path}")
            assert isinstance(methods, dict), f"Path '{path}' should contain method definitions"
            for method, definition in methods.items():
                logger.info(f"Validating HTTP method: {method}")
                assert method.lower() in ["get", "post", "put", "delete", "patch"], f"Invalid HTTP method '{method}'"
                assert isinstance(definition, dict), f"Method '{method}' definition should be object"
        
        logger.info("Schema JSON validity validation passed")
