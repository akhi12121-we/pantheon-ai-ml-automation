"""
Apollo API tests for welocalize.io
"""
import pytest
import sys
import time
from utils.http_client import APIClient
from utils.auth_helper import AuthHelper
from utils.logger import logger
from utils.ide_output_helper import ide_output
from utils.allure_helper import allure_helper
from config.settings import config

class TestApollo:
    """Apollo API test class."""
    
    def _force_print(self, message):
        """Force print output to be visible in IDE test runners."""
        print(message)
        sys.stdout.flush()
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test fixtures."""
        self.base_url = config.APOLLO_URL
        self.client = APIClient(self.base_url)
        
        # All Apollo endpoints defined in test file
        self.endpoints = {
            "health": "/health",
            "log_test": "/log_test", 
            "job_counts": "/job_counts"
        }
    
    def test_health_check(self):
        """Test Apollo health endpoint."""
        test_name = "test_health_check"
        start_time = time.time()
        logger.log_test_start(test_name)
        ide_output.test_info(test_name, "Starting health check test")
        
        try:
            endpoint = self.endpoints["health"]
            response = self.client.get(endpoint)
            
            # Assertions
            assert response.status_code == 200
            assert response.headers.get('content-type') == 'application/json'
            
            # Validate response body
            data = response.json()
            assert data["status"] == "ok"
            
            # Multiple output methods for IDE visibility
            logger.info(f"Health check response: {data}")
            ide_output.force_print(f"Health check response: {data}")
            ide_output.test_result(test_name, "PASSED", f"Response: {data}")
            logger.log_test_end(test_name, "PASSED")
            
            # Generate Allure result
            allure_helper.generate_test_result(
                test_name=test_name,
                status="passed",
                start_time=start_time,
                end_time=time.time()
            )
            
        except Exception as e:
            # Generate failed Allure result
            allure_helper.generate_test_result(
                test_name=test_name,
                status="failed",
                start_time=start_time,
                end_time=time.time(),
                error_message=str(e)
            )
            raise
    
    def test_log_test(self):
        """Test Apollo log_test endpoint."""
        test_name = "test_log_test"
        logger.log_test_start(test_name)
        ide_output.test_info(test_name, "Starting log test")
        
        endpoint = self.endpoints["log_test"]
        response = self.client.get(endpoint)
        
        # Assertions
        assert response.status_code == 200
        assert response.headers.get('content-type') == 'application/json'
        
        # Log response with multiple output methods
        data = response.json()
        logger.info(f"Log test response: {data}")
        ide_output.force_print(f"Log test response: {data}")
        ide_output.test_result(test_name, "PASSED", f"Response: {data}")
        logger.log_test_end(test_name, "PASSED")
    
    def test_job_counts(self):
        """Test Apollo job_counts endpoint."""
        logger.log_test_start("test_job_counts")
        
        endpoint = self.endpoints["job_counts"]
        response = self.client.get(endpoint)
        
        # Assertions
        assert response.status_code == 200
        assert response.headers.get('content-type') == 'application/json'
        
        # Log response
        data = response.json()
        logger.info(f"Job counts response: {data}")
        logger.log_test_end("test_job_counts", "PASSED")
    
    def test_all_endpoints_together(self):
        """Test all Apollo endpoints in sequence."""
        test_endpoints = [
            (self.endpoints["health"], {"status": "ok"}),
            (self.endpoints["log_test"], None),
            (self.endpoints["job_counts"], None)
        ]
        
        for endpoint, expected_data in test_endpoints:
            response = self.client.get(endpoint)
            
            # Basic assertions
            assert response.status_code == 200
            assert response.headers.get('content-type') == 'application/json'
            
            # Validate specific data if expected
            if expected_data:
                data = response.json()
                for key, value in expected_data.items():
                    assert data[key] == value
            
            logger.log_test_end(f"test_all_endpoints_together {endpoint}", "PASSED")
    
    def test_response_times(self):
        """Test response times for Apollo endpoints."""
        import time
        
        endpoints = list(self.endpoints.values())
        
        for endpoint in endpoints:
            start_time = time.time()
            response = self.client.get(endpoint)
            end_time = time.time()
            
            response_time = end_time - start_time
            
            # Assertions
            assert response.status_code == 200
            assert response_time < 5.0  # Should respond within 5 seconds
            
            logger.info(f"{endpoint} - Response time: {response_time:.2f}s")
    
    def test_headers(self):
        """Test that proper headers are sent."""
        endpoint = self.endpoints["health"]
        response = self.client.get(endpoint)
        
        # Check request headers were sent correctly
        assert response.status_code == 200
        
        # Verify response headers
        assert 'content-type' in response.headers
        assert response.headers['content-type'] == 'application/json'
        
        logger.info("Headers test passed")
        logger.log_test_end("test_headers", "PASSED")
