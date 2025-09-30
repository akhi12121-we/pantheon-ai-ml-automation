"""
Custom Allure Helper for generating Allure results without the problematic plugin.
"""
import json
import uuid
import time
import os
import shutil
from datetime import datetime
from typing import Dict, Any, List


class AllureHelper:
    """Helper class to generate Allure results manually."""
    
    def __init__(self, results_dir: str = "allure-results"):
        self.results_dir = results_dir
        os.makedirs(results_dir, exist_ok=True)
    
    def clean_results(self):
        """Clean all existing Allure results."""
        if os.path.exists(self.results_dir):
            shutil.rmtree(self.results_dir)
            print(f"🧹 Cleaned existing Allure results from {self.results_dir}")
        
        # Recreate the directory
        os.makedirs(self.results_dir, exist_ok=True)
        print(f"📁 Created fresh Allure results directory: {self.results_dir}")
    
    def clean_old_results(self, older_than_minutes: int = 5):
        """Clean Allure results older than specified minutes."""
        if not os.path.exists(self.results_dir):
            return
        
        current_time = time.time()
        cutoff_time = current_time - (older_than_minutes * 60)
        
        cleaned_count = 0
        for filename in os.listdir(self.results_dir):
            file_path = os.path.join(self.results_dir, filename)
            if os.path.isfile(file_path):
                file_time = os.path.getmtime(file_path)
                if file_time < cutoff_time:
                    os.remove(file_path)
                    cleaned_count += 1
        
        if cleaned_count > 0:
            print(f"🧹 Cleaned {cleaned_count} old Allure result files (older than {older_than_minutes} minutes)")
        else:
            print(f"✅ No old Allure results to clean (all files are newer than {older_than_minutes} minutes)")
    
    def generate_test_result(self, test_name: str, status: str, 
                           start_time: float = None, end_time: float = None,
                           error_message: str = None, attachments: List[Dict] = None,
                           test_class: str = None, package: str = None, suite: str = None) -> str:
        """Generate a test result JSON file for Allure."""
        
        if start_time is None:
            start_time = time.time()
        if end_time is None:
            end_time = time.time()
        
        test_uuid = str(uuid.uuid4())
        
        # Convert timestamps to milliseconds
        start_time_ms = int(start_time * 1000)
        end_time_ms = int(end_time * 1000)
        
        # Auto-detect test type and suite name if not provided
        if not test_class:
            test_class = self._detect_test_class(test_name)
        if not package:
            package = self._detect_package(test_name)
        if not suite:
            suite = self._detect_suite_name(test_name)
        
        result = {
            "uuid": test_uuid,
            "name": test_name,
            "status": status.lower(),
            "statusDetails": {},
            "stage": "finished",
            "start": start_time_ms,
            "stop": end_time_ms,
            "steps": [],
            "attachments": attachments or [],
            "parameters": [],
            "labels": [
                {
                    "name": "testClass",
                    "value": test_class
                },
                {
                    "name": "testMethod", 
                    "value": test_name
                },
                {
                    "name": "package",
                    "value": package
                },
                {
                    "name": "suite",
                    "value": suite
                }
            ]
        }
        
        if error_message:
            result["statusDetails"] = {
                "message": error_message,
                "trace": error_message
            }
        
        # Write result file
        result_file = os.path.join(self.results_dir, f"{test_uuid}-result.json")
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2)
        
        return test_uuid
    
    def generate_container(self, test_uuid: str, test_name: str) -> str:
        """Generate a container JSON file for Allure."""
        
        container_uuid = str(uuid.uuid4())
        
        container = {
            "uuid": container_uuid,
            "name": test_name,
            "children": [test_uuid],
            "befores": [],
            "afters": []
        }
        
        # Write container file
        container_file = os.path.join(self.results_dir, f"{container_uuid}-container.json")
        with open(container_file, 'w', encoding='utf-8') as f:
            json.dump(container, f, indent=2)
        
        return container_uuid
    
    def _detect_test_class(self, test_name: str) -> str:
        """Auto-detect test class based on test name."""
        if "apollo" in test_name.lower():
            return "TestApollo"
        elif "ui" in test_name.lower() or "browser" in test_name.lower():
            return "UITest"
        elif "api" in test_name.lower():
            return "APITest"
        else:
            return "TestSuite"
    
    def _detect_package(self, test_name: str) -> str:
        """Auto-detect package based on test name."""
        if "apollo" in test_name.lower():
            return "tests.api.test_apollo"
        elif "ui" in test_name.lower() or "browser" in test_name.lower():
            return "tests.ui"
        elif "api" in test_name.lower():
            return "tests.api"
        else:
            return "tests"
    
    def _detect_suite_name(self, test_name: str) -> str:
        """Auto-detect suite name based on test name."""
        if "apollo" in test_name.lower():
            return "Apollo API Tests"
        elif "ui" in test_name.lower() or "browser" in test_name.lower():
            return "UI Tests"
        elif "api" in test_name.lower():
            return "API Tests"
        else:
            return "Test Suite"


# Global instance
allure_helper = AllureHelper()
