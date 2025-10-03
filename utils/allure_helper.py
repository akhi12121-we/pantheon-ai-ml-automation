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
                           test_class: str = None, package: str = None, suite: str = None,
                           log_file: str = None) -> str:
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
        
        # Get real logger steps from log file
        steps = self._get_logger_steps(log_file, test_name, start_time_ms, end_time_ms)
        all_attachments = attachments or []
        
        result = {
            "uuid": test_uuid,
            "name": test_name,
            "status": status.lower(),
            "statusDetails": {},
            "stage": "finished",
            "start": start_time_ms,
            "stop": end_time_ms,
            "steps": steps,
            "attachments": all_attachments,
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
    
    def _generate_steps_from_logs(self, log_file: str, start_time_ms: int, end_time_ms: int, test_name: str = None) -> List[Dict]:
        """Generate Allure steps from log file filtered by test name patterns."""
        steps = []
        
        if not log_file or not os.path.exists(log_file):
            return steps
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                log_lines = f.readlines()
            
            # Create test-specific patterns based on test name
            test_patterns = self._get_test_patterns(test_name)
            
            step_counter = 0
            seen_messages = set()  # Track seen messages to avoid duplicates
            
            for line in log_lines:
                # Look for relevant log entries (INFO, ERROR, WARNING)
                if ("INFO" in line or "ERROR" in line or "WARNING" in line) and ("automation_framework" in line):
                    # Check if this log line is related to the specific test
                    if self._is_test_related_log(line, test_patterns):
                        # Extract timestamp and message
                        parts = line.strip().split(' - ', 3)
                        if len(parts) >= 4:
                            timestamp_str = parts[0]
                            message = parts[3]
                            
                            # Skip generic messages that appear in multiple tests
                            if any(generic in message.lower() for generic in ["row 1 - date", "status: succes", "jobs table found"]):
                                continue
                            
                            # Skip duplicate messages
                            if message in seen_messages:
                                continue
                            seen_messages.add(message)
                            
                            step_counter += 1
                            
                            # Create step
                            step = {
                                "name": f"Step {step_counter}: {message[:50]}...",
                                "status": "passed" if "INFO" in line else "failed" if "ERROR" in line else "broken",
                                "stage": "finished",
                                "start": start_time_ms + (step_counter * 1000),
                                "stop": start_time_ms + (step_counter * 1000) + 100,
                                "steps": [],
                                "attachments": []
                            }
                            
                            steps.append(step)
            
        except Exception as e:
            print(f"⚠️ Error generating steps from logs: {e}")
        
        return steps
    
    def _get_test_patterns(self, test_name: str) -> List[str]:
        """Get test-specific patterns to filter logs."""
        if not test_name:
            return []
        
        patterns = []
        test_lower = test_name.lower()
        
        # Very specific patterns for each test - only unique keywords that don't appear in other tests
        if "create xtm project" in test_lower:
            patterns.extend(["XTM", "Add project", "customer dropdown", "source language", "target language", "workflow", "file uploaded", "Create button", "XTM login"])
        elif "create scheduler job" in test_lower:
            patterns.extend(["scheduler", "developer", "platform", "JSON", "Submit", "Refresh", "junction", "authenticate", "payload", "platformInstanceId", "Create Job", "job creation"])
        elif "search project relay" in test_lower:
            patterns.extend(["relay", "Welocalize", "Projects link", "All projects", "search term", "project link", "relay page", "searching for project"])
        
        return patterns
    
    def _is_test_related_log(self, log_line: str, test_patterns: List[str]) -> bool:
        """Check if log line is related to specific test."""
        if not test_patterns:
            return False  # Don't show any logs if no patterns
        
        log_lower = log_line.lower()
        # Use more strict matching - log must contain at least one pattern
        return any(pattern.lower() in log_lower for pattern in test_patterns)
    
    def _get_basic_steps(self, test_name: str, start_time_ms: int, end_time_ms: int) -> List[Dict]:
        """Get basic steps for test without parsing logs."""
        steps = [
            {
                "name": f"Starting {test_name}",
                "status": "passed",
                "stage": "finished",
                "start": start_time_ms,
                "stop": start_time_ms + 100,
                "steps": [],
                "attachments": []
            },
            {
                "name": f"Executing {test_name}",
                "status": "passed",
                "stage": "finished", 
                "start": start_time_ms + 100,
                "stop": start_time_ms + 200,
                "steps": [],
                "attachments": []
            },
            {
                "name": f"Completed {test_name}",
                "status": "passed",
                "stage": "finished",
                "start": start_time_ms + 200,
                "stop": end_time_ms,
                "steps": [],
                "attachments": []
            }
        ]
        return steps
    
    def _get_logger_steps(self, log_file: str, test_name: str, start_time_ms: int, end_time_ms: int) -> List[Dict]:
        """Get real logger steps from log file for specific test."""
        steps = []
        
        if not log_file or not os.path.exists(log_file):
            return steps
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                log_lines = f.readlines()
            
            step_counter = 0
            for line in log_lines:
                # Look for INFO logs from automation_framework
                if "INFO" in line and "automation_framework" in line:
                    # Extract timestamp and message
                    parts = line.strip().split(' - ', 3)
                    if len(parts) >= 4:
                        timestamp_str = parts[0]
                        message = parts[3]
                        
                        # Parse timestamp to check if log is within test execution time
                        try:
                            # Parse timestamp like "2025-01-03 16:21:53,123"
                            log_time = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S,%f")
                            log_time_ms = int(log_time.timestamp() * 1000)
                            
                            # Only include logs that occurred during this test execution
                            if start_time_ms <= log_time_ms <= end_time_ms:
                                step_counter += 1
                                
                                # Create step from real log message
                                step = {
                                    "name": f"Step {step_counter}: {message[:60]}...",
                                    "status": "passed",
                                    "stage": "finished",
                                    "start": log_time_ms,
                                    "stop": log_time_ms + 100,
                                    "steps": [],
                                    "attachments": []
                                }
                                
                                steps.append(step)
                        except ValueError:
                            # Skip lines with invalid timestamps
                            continue
            
        except Exception as e:
            print(f"⚠️ Error getting logger steps: {e}")
        
        return steps
    
    def _is_test_related_log_simple(self, log_line: str, test_name: str) -> bool:
        """Simple check if log line is related to specific test."""
        test_lower = test_name.lower()
        log_lower = log_line.lower()
        
        # Simple pattern matching for each test
        if "create xtm project" in test_lower:
            return any(keyword in log_lower for keyword in ["xtm", "project", "login", "browser", "add project", "customer", "source language", "target language", "workflow", "file uploaded"])
        elif "create scheduler job" in test_lower:
            return any(keyword in log_lower for keyword in ["scheduler", "developer", "platform", "json", "submit", "refresh", "junction", "authenticate", "payload", "create job"])
        elif "search project relay" in test_lower:
            return any(keyword in log_lower for keyword in ["relay", "welocalize", "projects link", "all projects", "search", "project link", "searching"])
        
        return False
    
    def _create_log_attachment(self, log_file: str, attachment_name: str = None) -> Dict:
        """Create Allure attachment from log file."""
        if not log_file or not os.path.exists(log_file):
            return None
        
        try:
            # Copy log file to allure-results directory
            if not attachment_name:
                attachment_name = f"test_log_{int(time.time())}.txt"
            
            attachment_path = os.path.join(self.results_dir, attachment_name)
            shutil.copy2(log_file, attachment_path)
            
            return {
                "name": "Test Log",
                "type": "text/plain",
                "source": attachment_name
            }
            
        except Exception as e:
            print(f"⚠️ Error creating log attachment: {e}")
            return None


# Global instance
allure_helper = AllureHelper()
