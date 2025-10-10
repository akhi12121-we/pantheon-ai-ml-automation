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
                           log_file: str = None, retry_count: int = 0) -> str:
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
        
        # Add log file as attachment if it exists
        all_attachments = attachments or []
        if log_file and os.path.exists(log_file):
            log_attachment = self._create_log_attachment(log_file, f"{test_name.replace(' ', '_')}_log.txt")
            if log_attachment:
                all_attachments.append(log_attachment)
        
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
        
        # Add retry information if retries occurred
        if retry_count > 0:
            retry_entries = []
            for i in range(retry_count):
                retry_uuid = str(uuid.uuid4())
                retry_entry = {
                    "uuid": retry_uuid,
                    "name": f"{test_name} (Attempt {i+1})",
                    "status": "failed" if i < retry_count - 1 else status.lower(),
                    "stage": "finished",
                    "start": start_time_ms + (i * 1000),
                    "stop": start_time_ms + ((i + 1) * 1000),
                    "steps": [
                        {
                            "name": f"Retry Attempt {i+1}",
                            "status": "failed" if i < retry_count - 1 else status.lower(),
                            "stage": "finished",
                            "start": start_time_ms + (i * 1000),
                            "stop": start_time_ms + ((i + 1) * 1000),
                            "steps": [],
                            "attachments": []
                        }
                    ],
                    "attachments": []
                }
                retry_entries.append(retry_entry)
            
            result["retries"] = retry_entries
        
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
    
    def _get_basic_steps(self, test_name: str, start_time_ms: int, end_time_ms: int) -> List[Dict]:
        """Get basic steps for test without parsing logs."""
        duration = end_time_ms - start_time_ms
        step_duration = max(100, duration // 5)  # Divide duration into 5 steps
        
        steps = [
            {
                "name": f"Step 1: Starting {test_name}",
                "status": "passed",
                "stage": "finished",
                "start": start_time_ms,
                "stop": start_time_ms + step_duration,
                "steps": [],
                "attachments": []
            },
            {
                "name": f"Step 2: Initializing test execution",
                "status": "passed",
                "stage": "finished",
                "start": start_time_ms + step_duration,
                "stop": start_time_ms + (step_duration * 2),
                "steps": [],
                "attachments": []
            },
            {
                "name": f"Step 3: Running {test_name}",
                "status": "passed",
                "stage": "finished",
                "start": start_time_ms + (step_duration * 2),
                "stop": start_time_ms + (step_duration * 3),
                "steps": [],
                "attachments": []
            },
            {
                "name": f"Step 4: Processing test results",
                "status": "passed",
                "stage": "finished",
                "start": start_time_ms + (step_duration * 3),
                "stop": start_time_ms + (step_duration * 4),
                "steps": [],
                "attachments": []
            },
            {
                "name": f"Step 5: Completed {test_name}",
                "status": "passed",
                "stage": "finished",
                "start": start_time_ms + (step_duration * 4),
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
            print(f"⚠️ Log file not found: {log_file}")
            return self._get_basic_steps(test_name, start_time_ms, end_time_ms)
        
        try:
            # Try different encodings to handle the UTF-8 decode error
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            log_lines = []
            
            for encoding in encodings:
                try:
                    with open(log_file, 'r', encoding=encoding) as f:
                        log_lines = f.readlines()
                    break
                except UnicodeDecodeError:
                    continue
            
            if not log_lines:
                print(f"⚠️ No log lines found in {log_file}")
                return self._get_basic_steps(test_name, start_time_ms, end_time_ms)
            
            step_counter = 0
            seen_messages = set()
            
            # Get clean test name without retry info
            clean_test_name = test_name.split(" (Attempts:")[0].strip()
            
            # STRICT filtering: Only include logs that are clearly from this specific test
            for line in log_lines:
                if "INFO" in line and "automation_framework" in line:
                    parts = line.strip().split(' - ', 3)
                    if len(parts) >= 4:
                        message = parts[3]
                        
                        # Skip duplicate messages
                        if message in seen_messages:
                            continue
                        seen_messages.add(message)
                        
                        # Skip very short messages
                        if len(message.strip()) < 10:
                            continue
                        
                        # STRICT test-specific filtering
                        if self._is_log_for_this_test(message, clean_test_name):
                            step_counter += 1
                            
                            # Create step from real log message
                            step = {
                                "name": f"Step {step_counter}: {message}",
                                "status": "passed",
                                "stage": "finished",
                                "start": start_time_ms + (step_counter * 1000),
                                "stop": start_time_ms + (step_counter * 1000) + 100,
                                "steps": [],
                                "attachments": []
                            }
                            
                            steps.append(step)
            
            # If still no steps, add basic steps
            if not steps:
                print(f"⚠️ No test-specific logs found for {clean_test_name}, adding basic steps")
                steps = self._get_basic_steps(test_name, start_time_ms, end_time_ms)
            
        except Exception as e:
            print(f"⚠️ Error getting logger steps: {e}")
            steps = self._get_basic_steps(test_name, start_time_ms, end_time_ms)
        
        return steps
    
    def _is_log_for_this_test(self, message: str, test_name: str) -> bool:
        """Strict check if log message belongs to this specific test."""
        message_lower = message.lower()
        test_lower = test_name.lower()
        
        # Very specific patterns for each test
        if "search project relay" in test_lower:
            # Only logs that are clearly from Search Project Relay test
            return any(keyword in message_lower for keyword in [
                "search project relay", "searching for project", "relay", "welocalize", 
                "projects link", "all projects", "search term", "project link"
            ])
        elif "verify pulled project production status" in test_lower:
            # Only logs that are clearly from Production Status test
            return any(keyword in message_lower for keyword in [
                "verify pulled project production status", "production status", "pulled project",
                "verify production", "production verification", "starting test verify pulled"
            ])
        elif "create xtm project" in test_lower:
            # Only logs that are clearly from XTM Project Creation test
            return any(keyword in message_lower for keyword in [
                "create xtm project", "xtm project creation", "add project", "xtm login",
                "customer dropdown", "source language", "target language", "workflow"
            ])
        elif "create scheduler job" in test_lower:
            # Only logs that are clearly from Scheduler Job test
            return any(keyword in message_lower for keyword in [
                "create scheduler job", "scheduler job", "developer", "platform", "json",
                "submit", "refresh", "junction", "authenticate", "payload"
            ])
        elif "project search and segment" in test_lower:
            # Only logs that are clearly from Project Search and Segment test
            return any(keyword in message_lower for keyword in [
                "project search and segment", "search project", "segment navigation",
                "manage jobs", "right-click", "lock icon", "click segment"
            ])
        elif "verify ai task" in test_lower:
            # Only logs that are clearly from AI Task test
            return any(keyword in message_lower for keyword in [
                "verify ai task", "ai task", "ai verification", "task verification"
            ])
        elif "verify mt copy edit" in test_lower:
            # Only logs that are clearly from MT Copy Edit test
            return any(keyword in message_lower for keyword in [
                "verify mt copy edit", "mt copy edit", "mt count", "copy edit", "quote mt"
            ])
        
        # Default: be very restrictive
        return False
    
    def _get_test_specific_keywords(self, test_name: str) -> List[str]:
        """Get test-specific keywords for log filtering."""
        # Remove retry information from test name for keyword matching
        clean_test_name = test_name.split(" (Attempts:")[0].strip()
        clean_test_lower = clean_test_name.lower()
        
        if "create xtm project" in clean_test_lower:
            return ["xtm", "project", "login", "browser", "add project", "customer", "source language", "target language", "workflow", "file uploaded", "create xtm", "xtm login", "project creation"]
        elif "create scheduler job" in clean_test_lower:
            return ["scheduler", "developer", "platform", "json", "submit", "refresh", "junction", "authenticate", "payload", "create job", "scheduler job", "job creation"]
        elif "search project relay" in clean_test_lower:
            return ["relay", "welocalize", "projects link", "all projects", "search", "project link", "searching", "relay page", "search project"]
        elif "verify pulled project production status" in clean_test_lower:
            return ["production", "status", "pulled", "project", "verify", "production status", "pulled project", "verify production", "production verification"]
        elif "verify ai task" in clean_test_lower:
            return ["ai", "task", "verification", "verify", "ai task", "task verification", "ai verification"]
        elif "project search and segment" in clean_test_lower:
            return ["search", "segment", "project", "navigation", "click", "segment navigation", "project search", "click segment", "manage jobs", "right-click", "lock icon"]
        elif "verify mt copy edit" in clean_test_lower:
            return ["mt", "copy", "edit", "count", "quote", "verify", "mt count", "copy edit", "mt copy", "quote mt"]
        else:
            # Generic keywords for unknown tests
            return ["step", "starting", "completed", "executing", "running", "test"]
    
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
