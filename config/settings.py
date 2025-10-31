"""
Configuration settings for API and UI automation.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for automation framework."""
    
    # ===========================================
    # API CONFIGURATION
    # ===========================================
    
    # API URLs
    # AIQE_URL = os.getenv("AIQE_URL", "https://aiqe-api.example.com")
    APOLLO_URL = os.getenv("APOLLO_URL", "https://apollo.welocalize.io")
    # COMET_URL = os.getenv("COMET_URL", "https://comet-api.example.com")
    OPAL_FASTAPI_URL = os.getenv("OPAL_FASTAPI_URL", "https://opal-api.welocalize.io")
    
    # Authentication
    AUTH_TOKEN = os.getenv("AUTH_TOKEN")
    AUTH_TOKEN_PANTHEON = "eyJqd3QiOiJleUpoYkdjaU9pSlNVekkxTmlJc0luUjVjQ0k2SWtwWFZDSXNJbU4wZVNJNklrcFhWQ0lzSW1wcmRTSTZJaUlzSW10cFpDSTZJaUo5LmV5SndZVzUwYUdWdmJrRjFkR2hVZVhCbElqb2lkWE5sY2lJc0ltOXJkR0ZKWkNJNkluWmhkMjkyYjJ3eE1EUkFhSEpoYVdacExtTnZiU0lzSW5CeWFXNWphWEJoYkNJNk56UTNOVGsxTENKaGRXUnBaVzVqWlNJNk1qRTFOellzSW1sdWRHVnlibUZzSWpwMGNuVmxMQ0p2Y21kaGJtbDZZWFJwYjI1SlpDSTZNakUxTnpZc0luSnZiR1Z6SWpwYkltRmtiV2x1SWl3aWRtVnVaRzl5TFcxaGJtRm5aWElpTENKa1pYWmxiRzl3WlhJaVhTd2libUZ0WlNJNklrOXViSGtnTkNCQmRYUnZiV0YwYVc5dUlDMGdSR1YyWld4dmNHVnlJQzBnVm1GM2IzWnZiQ0lzSW5WelpYSnVZVzFsSWpvaVQyNXNlU0EwSUVGMWRHOXRZWFJwYjI0Z0xTQkVaWFpsYkc5d1pYSWdMU0JXWVhkdmRtOXNJaXdpYzNSaGRIVnpJam9pWVdOMGFYWmxJaXdpYUdGelVtOWliM1JwWTB0bGVTSTZabUZzYzJVc0ltbGhkQ0k2TVRjMU9ESTVOekE1TXl3aWJtSm1Jam94TnpVNE1qazNNRGt6TENKbGVIQWlPakUzTmpBNU1qVXdPVE1zSW1semN5STZJblZ1YTI1dmQyNGlMQ0poZFdRaU9pSjFibXR1YjNkdUlpd2lhblJwSWpvaWFuZDBPblZ1WkdWbWFXNWxaQzh4TnpVNE1qazNNRGt6SW4wLlh4aWRKNkhsM2s3ZmV0YVQ2eWtzcTIwb0M0R3R1S0ZnMHUtWFFpZy1SODZBR3E1VDFkbVpqc29yMjRVWjBjbDVMbVBadFdYMzR5cWlwMzF1ZnIwWnQ2YWxXbFJWU2NUdEpDbElfeFozWTduV3BSeEZVOE5WX1VzRnhINVN1M0VsNlV3b0wtZTgyWkpYUy1hbFJ2LS13elFzSlhNZlN2Z0RDWWdZbkJfTUxBZVIzaWE1eTVJQndNSW1nQ0pVM0I0R29yY1ZKaTZaV2szQ2lxLUxodWVER1NZVUhJYW1nVWRWZnpQR2VBNzRUS2ZWdEItMy1qaXg0RVY4N0Q5MXBjTEZOeXZzUE9EVnliSkE0dThHSS1hNnFuSnJKbmFrR0RKclE4MEpvLWhtY1FVd1VoOXcwS3NjT0RSNXY3VVFfMG80c196clc3a0NkbkxSbUFUUmlnZ0UyZyIsImlzQXV0aGVudGljYXRlZCI6dHJ1ZSwiX2V4cGlyZSI6MTc4OTgzMzA5NDA3NSwiX21heEFnZSI6MzE1MzYwMDAwMDB9"
    AUTH_TOKEN_RELAY = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImN0eSI6IkpXVCIsImprdSI6IiIsImtpZCI6IiJ9.eyJwYW50aGVvbkF1dGhUeXBlIjoidXNlciIsIm9rdGFJZCI6InZhd292b2wxMDRAaHJhaWZpLmNvbSIsInByaW5jaXBhbCI6NzQ3NTk1LCJhdWRpZW5jZSI6MjE1NzYsImludGVybmFsIjp0cnVlLCJvcmdhbml6YXRpb25JZCI6MjE1NzYsInJvbGVzIjpbImFkbWluIiwidmVuZG9yLW1hbmFnZXIiLCJkZXZlbG9wZXIiXSwibmFtZSI6Ik9ubHkgNCBBdXRvbWF0aW9uIC0gRGV2ZWxvcGVyIC0gVmF3b3ZvbCIsInVzZXJuYW1lIjoiT25seSA0IEF1dG9tYXRpb24gLSBEZXZlbG9wZXIgLSBWYXdvdm9sIiwic3RhdHVzIjoiYWN0aXZlIiwiaGFzUm9ib3RpY0tleSI6ZmFsc2UsImlhdCI6MTc1ODI5NzA1OSwibmJmIjoxNzU4Mjk3MDU5LCJleHAiOjE3NjA5MjUwNTksImlzcyI6InVua25vd24iLCJhdWQiOiJ1bmtub3duIiwianRpIjoiand0OnVuZGVmaW5lZC8xNzU4Mjk3MDU5In0.uQHso28McOcB3KzKHm5JWePRSRudCCANhIkU_qKiy7C9_AjzIJwtGnmA25ZdkCfl1ToySkNwldZt-mEnGW5gTMpvR20uryP7fKBhZ6Gp0LB-1rKwP8GT1RouiIw_y4X90YDDQ7SGoc5vw9Z_s3Lu2GmJJ4HRKt5qXo6mVBSX8n7c9a1kayE9R224LdWDI9UXQVv2-JlW_MdPTORYTB4owoV-J6ZlwWTLrePjxKTHMmZdsv8eCn_KwdYUNGEmvLIH7wd9G9cffdpYxiScOVBmJ3NHVYM77cTxMqK9239NFuzK9CyKKvDx23dEBsf_LIu8mV1Vs2OWBFIgo9IaiJbOFQ"
    AUTH_CLIENT_TOKEN_OPAL  = "3a9103d99f55ea4a4e2b71cab921ea86ecc333f9521c67c36d905def2c8eb17d"
   
    # ==========================================
    # WEB UI CONFIGURATION
    # ==========================================
    
    # XTM Project Manager URL
    XTM_URL = os.getenv("XTM_URL", "https://word-uat.welocalize.com/project-manager-gui/login.jsp#!/login")
    
    # Pull Project in Pantheon Using UI Developer Tools
    PULL_PROJECT_URL = os.getenv("PULL_PROJECT_URL", "https://junction.welocalize.xyz/developer-admin/jobs/platform-get-projects/completed")
   
    # Pull project API URL Pantheon
    PULL_PROJECT_API_URL = os.getenv("PULL_PROJECT_API_URL", "https://atreus.welocalize.xyz")
    
    # Search Pulled Project in Relay
    SEARCH_PULLED_PROJECT_URL = os.getenv("SEARCH_PULLED_PROJECT_URL", "https://relay.welocalize.xyz/")
    
    # Base URLs for UI Testing
    BASE_URL = os.getenv("BASE_URL", "https://apollo.welocalize.io")
    PatheonURL = os.getenv("PatheonURL", "https://relay.welocalize.xyz/")
    
    # ===========================================
    # DATA CONFIGURATION
    # ===========================================
    
    # Data Paths
    DATA_ROOT = os.getenv("DATA_ROOT", "data")
    API_DATA_PATH = os.path.join(DATA_ROOT, "api")
    UI_DATA_PATH = os.path.join(DATA_ROOT, "ui")
    
    # API Data Paths
    API_REQUESTS_PATH = os.path.join(API_DATA_PATH, "requests")
    API_RESPONSES_PATH = os.path.join(API_DATA_PATH, "responses")
    
    # UI Data Paths
    UI_TESTDATA_PATH = os.path.join(UI_DATA_PATH, "testdata")
    
    # ===========================================
    # UI AUTOMATION CONFIGURATION
    # ===========================================
    
    # Browser Configuration
    BROWSER_TYPE = os.getenv("BROWSER_TYPE", "chromium")
    HEADLESS_MODE = os.getenv("HEADLESS_MODE", "true").lower()
    RUN_HEADLESS = os.getenv("RUN_HEADLESS", "true").lower() == "true"
    
    # ===========================================
    # TIMEOUT CONFIGURATION
    # ===========================================
    
    # UI Timeouts (in milliseconds)
    DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "30000"))
    NAVIGATION_TIMEOUT = int(os.getenv("NAVIGATION_TIMEOUT", "60000"))
    ELEMENT_TIMEOUT = int(os.getenv("ELEMENT_TIMEOUT", "30000"))
    
    # ===========================================
    # RETRY CONFIGURATION
    # ===========================================
    
    # UI Retries
    UI_RETRY_DELAY = float(os.getenv("UI_RETRY_DELAY", "1.0"))
    
    # Element Interaction Retries
    CLICK_RETRY_COUNT = int(os.getenv("CLICK_RETRY_COUNT", "3"))
    FILL_RETRY_COUNT = int(os.getenv("FILL_RETRY_COUNT", "3"))
    WAIT_RETRY_COUNT = int(os.getenv("WAIT_RETRY_COUNT", "5"))
    
    # Interaction Delays
    CLICK_DELAY = int(os.getenv("CLICK_DELAY", "0"))
    TYPE_DELAY = int(os.getenv("TYPE_DELAY", "0"))
    
    # Navigation Settings
    WAIT_FOR_NAVIGATION = os.getenv("WAIT_FOR_NAVIGATION", "networkidle").lower()
    WAIT_FOR_LOAD_STATE = os.getenv("WAIT_FOR_LOAD_STATE", "networkidle").lower()
    
    # ===========================================
    # SCREENSHOT CONFIGURATION
    # ===========================================
    
    # Screenshot Settings
    SCREENSHOT_ON_FAILURE = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"
    SCREENSHOT_FULL_PAGE = os.getenv("SCREENSHOT_FULL_PAGE", "true").lower() == "true"
    SCREENSHOT_PATH = os.getenv("SCREENSHOT_PATH", "screenshots")
    SCREENSHOT_FORMAT = os.getenv("SCREENSHOT_FORMAT", "png")
    SCREENSHOT_QUALITY = int(os.getenv("SCREENSHOT_QUALITY", "90"))
    SCREENSHOT_INCLUDE_TEST_NAME = os.getenv("SCREENSHOT_INCLUDE_TEST_NAME", "true").lower() == "true"
    SCREENSHOT_INCLUDE_TIMESTAMP = os.getenv("SCREENSHOT_INCLUDE_TIMESTAMP", "true").lower() == "true"
    SCREENSHOT_FAILED_TESTS_ONLY = os.getenv("SCREENSHOT_FAILED_TESTS_ONLY", "true").lower() == "true"
    
    # ===========================================
    # VIDEO RECORDING CONFIGURATION
    # ===========================================
    
    # Video Recording Settings
    VIDEO_RECORDING = os.getenv("VIDEO_RECORDING", "true").lower() == "false"
    VIDEO_PATH = os.getenv("VIDEO_PATH", "videos")
    VIDEO_FORMAT = os.getenv("VIDEO_FORMAT", "webm")
    
    # Performance and Network Monitoring
    ENABLE_PERFORMANCE_MONITORING = os.getenv("ENABLE_PERFORMANCE_MONITORING", "false").lower() == "true"
    ENABLE_NETWORK_MONITORING = os.getenv("ENABLE_NETWORK_MONITORING", "false").lower() == "true"
    LOG_NETWORK_REQUESTS = os.getenv("LOG_NETWORK_REQUESTS", "false").lower() == "true"
    
    # ===========================================
    # LOGGING CONFIGURATION
    # ===========================================
    
    # Logging Settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # ===========================================
    # UTILITY METHODS
    # ===========================================
    
    @classmethod
    def get_headless_mode(cls):
        """Get headless mode setting."""
        if hasattr(cls, 'RUN_HEADLESS') and cls.RUN_HEADLESS is not None:
            return cls.RUN_HEADLESS
        
        if cls.HEADLESS_MODE == "auto":
            return cls.RUN_HEADLESS
        elif cls.HEADLESS_MODE == "true":
            return True
        elif cls.HEADLESS_MODE == "false":
            return False
        else:
            return cls.RUN_HEADLESS
    
    @classmethod
    def should_take_screenshots(cls):
        """Check if screenshots should be taken."""
        return cls.SCREENSHOT_ON_FAILURE
    
    @classmethod
    def should_take_screenshot_for_failure(cls):
        """Check if screenshot should be taken for failed tests only."""
        return cls.SCREENSHOT_ON_FAILURE and cls.SCREENSHOT_FAILED_TESTS_ONLY

# Global config instance
config = Config()