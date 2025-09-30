"""
Simple HTTP client for API testing.
"""
import requests
import time
from typing import Dict, Any, Optional
from utils.auth_helper import AuthHelper
from utils.logger import logger

class APIClient:
    """Simple API client."""
    
    def __init__(self, base_url: str, auth: Optional[AuthHelper] = None):
        self.base_url = base_url.rstrip('/')
        self.auth = auth or AuthHelper()
        self.session = requests.Session()
    
    def set_auth(self, auth: AuthHelper):
        """Set authentication for this client."""
        self.auth = auth
        return self
    
    def _get_headers(self, custom_headers: Dict[str, str] = None) -> Dict[str, str]:
        """Get headers with authentication."""
        headers = {"Content-Type": "application/json"}
        headers.update(self.auth.get_headers())
        if custom_headers:
            headers.update(custom_headers)
        return headers
    
    def _build_url(self, endpoint: str) -> str:
        """Build full URL."""
        if endpoint.startswith('http'):
            return endpoint
        endpoint = endpoint.lstrip('/')
        return f"{self.base_url}/{endpoint}"
    
    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Make HTTP request with logging."""
        start_time = time.time()
        
        try:
            response = self.session.request(method, url, **kwargs)
            response_time = time.time() - start_time
            
            # Log request
            logger.log_request(method, url, response.status_code, response_time)
            
            return response
            
        except requests.exceptions.RequestException as e:
            response_time = time.time() - start_time
            logger.error(f"Request failed: {method} {url} - Error: {str(e)} - Time: {response_time:.2f}s")
            raise
    
    def get(self, endpoint: str, params: Dict[str, Any] = None, headers: Dict[str, str] = None) -> requests.Response:
        """GET request."""
        url = self._build_url(endpoint)
        return self._make_request('GET', url, params=params, headers=self._get_headers(headers))
    
    def post(self, endpoint: str, data: Dict[str, Any] = None, headers: Dict[str, str] = None) -> requests.Response:
        """POST request."""
        url = self._build_url(endpoint)
        return self._make_request('POST', url, json=data, headers=self._get_headers(headers))
    
    def put(self, endpoint: str, data: Dict[str, Any] = None, headers: Dict[str, str] = None) -> requests.Response:
        """PUT request."""
        url = self._build_url(endpoint)
        return self._make_request('PUT', url, json=data, headers=self._get_headers(headers))
    
    def patch(self, endpoint: str, data: Dict[str, Any] = None, headers: Dict[str, str] = None) -> requests.Response:
        """PATCH request."""
        url = self._build_url(endpoint)
        return self._make_request('PATCH', url, json=data, headers=self._get_headers(headers))
    
    def delete(self, endpoint: str, headers: Dict[str, str] = None) -> requests.Response:
        """DELETE request."""
        url = self._build_url(endpoint)
        return self._make_request('DELETE', url, headers=self._get_headers(headers))