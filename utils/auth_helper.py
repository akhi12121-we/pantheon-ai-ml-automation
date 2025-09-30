"""
Simple authentication helper.
"""
from typing import Dict, Optional

class AuthHelper:
    """Simple authentication helper."""
    
    def __init__(self, token: Optional[str] = None):
        self.token = token
    
    def set_token(self, token: str):
        """Set authentication token."""
        self.token = token
    
    def get_headers(self) -> Dict[str, str]:
        """Get authentication headers."""
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}
    
    def is_authenticated(self) -> bool:
        """Check if authenticated."""
        return bool(self.token)