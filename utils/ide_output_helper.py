"""
IDE Output Helper for ensuring test output visibility in Cursor IDE.
"""
import sys
import os
from typing import Any


class IDEOutputHelper:
    """Helper class to ensure output is visible in IDE test runners."""
    
    @staticmethod
    def force_print(message: str, flush: bool = True):
        """Force print output to be visible in IDE."""
        print(message, flush=flush)
        if flush:
            sys.stdout.flush()
            sys.stderr.flush()
    
    @staticmethod
    def force_log(logger, level: str, message: str):
        """Force log output to be visible in IDE."""
        log_method = getattr(logger, level.lower(), logger.info)
        log_method(message)
        sys.stdout.flush()
        sys.stderr.flush()
    
    @staticmethod
    def debug_output(message: str, **kwargs):
        """Debug output that's always visible."""
        print(f"[DEBUG] {message}", flush=True)
        if kwargs:
            for key, value in kwargs.items():
                print(f"[DEBUG] {key}: {value}", flush=True)
        sys.stdout.flush()
    
    @staticmethod
    def test_info(test_name: str, message: str):
        """Test-specific info output."""
        print(f"[TEST: {test_name}] {message}", flush=True)
        sys.stdout.flush()
    
    @staticmethod
    def test_result(test_name: str, status: str, details: str = ""):
        """Test result output."""
        result_msg = f"[RESULT: {test_name}] {status}"
        if details:
            result_msg += f" - {details}"
        print(result_msg, flush=True)
        sys.stdout.flush()


# Global instance
ide_output = IDEOutputHelper()
