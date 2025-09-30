"""
Logging utility for the automation framework.
"""
import logging
import os
import sys
from datetime import datetime
from config.settings import config

class Logger:
    """Simple logger for automation framework."""
    
    def __init__(self, name: str = "automation_framework"):
        self.name = name
        self.logger = logging.getLogger(name)
        self._setup_logger()
    
    def _setup_logger(self):
        """Setup logger configuration."""
        # Create logs directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)
        
        # Set log level
        log_level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)
        self.logger.setLevel(log_level)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console handler - Force stdout for IDE compatibility
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File handler
        log_file = f"logs/automation_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Ensure logs are flushed immediately
        self.logger.propagate = True
    
    def info(self, message: str):
        """Log info message."""
        self.logger.info(message)
        # Force flush for IDE compatibility
        sys.stdout.flush()
    
    def debug(self, message: str):
        """Log debug message."""
        self.logger.debug(message)
        sys.stdout.flush()
    
    def warning(self, message: str):
        """Log warning message."""
        self.logger.warning(message)
        sys.stdout.flush()
    
    def error(self, message: str):
        """Log error message."""
        self.logger.error(message)
        sys.stdout.flush()
    
    def critical(self, message: str):
        """Log critical message."""
        self.logger.critical(message)
        sys.stdout.flush()
    
    def log_request(self, method: str, url: str, status_code: int = None, response_time: float = None):
        """Log HTTP request details."""
        if status_code and response_time:
            self.info(f"{method.upper()} {url} - Status: {status_code} - Time: {response_time:.2f}s")
        else:
            self.info(f"{method.upper()} {url}")
    
    def log_test_start(self, test_name: str):
        """Log test start."""
        self.info(f"[START] Starting test: {test_name}")
    
    def log_test_end(self, test_name: str, status: str):
        """Log test end."""
        self.info(f"[{status}] Test completed: {test_name}")

# Global logger instance
logger = Logger()
