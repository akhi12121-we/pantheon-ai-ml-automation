#!/usr/bin/env python3
"""
Utility module for running tests with retry logic.
"""
import subprocess
import sys
import os
import time
from datetime import datetime
from utils.allure_helper import allure_helper


def run_test(test_path, test_name):
    """Run a specific test with Allure result generation."""
    print(f"\n{'='*60}")
    print(f"Running: {test_name}")
    print(f"{'='*60}")
    
    cmd = [
        sys.executable, "-m", "pytest", 
        test_path, 
        "-v", "-s", 
        "--tb=short"
    ]
    
    # Set PYTHONPATH
    env = os.environ.copy()
    env['PYTHONPATH'] = os.getcwd()
    
    # Record test start time
    test_start_time = time.time()
    
    result = subprocess.run(cmd, env=env)
    
    # Record test end time
    test_end_time = time.time()
    
    # Generate Allure result with real logger steps
    try:
        status = "passed" if result.returncode == 0 else "failed"
        log_file = f"logs/automation_{datetime.now().strftime('%Y%m%d')}.log"
        
        allure_helper.generate_test_result(
            test_name=test_name,
            status=status,
            test_class="UITest",
            package="tests.ui",
            suite="UI Project Creation Tests",
            log_file=log_file,
            start_time=test_start_time,
            end_time=test_end_time
        )
    except Exception as e:
        print(f"⚠️ Could not generate Allure result: {e}")
    
    return result.returncode


def run_test_with_retry(test_path, test_name, max_retries=1, wait_before_seconds=0, wait_between_retries_seconds=0):
    """Run a test with retry logic."""
    if wait_before_seconds > 0:
        print(f"⏳ Waiting {wait_before_seconds} seconds before running {test_name}...")
        time.sleep(wait_before_seconds)
    
    # Record overall test start time for Allure
    overall_start_time = time.time()
    final_result = 1  # Default to failure
    attempt_count = 0
    
    # Use consistent log file path for all attempts
    log_file = f"logs/automation_{datetime.now().strftime('%Y%m%d')}.log"
    
    for attempt in range(1, max_retries + 1):
        attempt_count = attempt
        if attempt > 1:
            print(f"\n🔄 Attempt {attempt}/{max_retries}: {test_name}")
        else:
            print(f"\n{attempt}. Running {test_name}")
        
        # Run test without generating Allure result for each attempt
        result = run_test_without_allure(test_path, test_name)
        
        if result == 0:
            print(f"✅ {test_name} successful!")
            final_result = 0
            break
        else:
            print(f"❌ {test_name} failed on attempt {attempt}")
            if attempt < max_retries:
                if wait_between_retries_seconds > 0:
                    print(f"⏳ Waiting {wait_between_retries_seconds} seconds before retry {attempt + 1}...")
                    time.sleep(wait_between_retries_seconds)
            else:
                print(f"❌ All retry attempts failed for {test_name}!")
                final_result = result
    
    # Log test completion (Playwright will handle HTML reporting)
    overall_end_time = time.time()
    duration = overall_end_time - overall_start_time
    
    if attempt_count > 1:
        print(f"📊 Test '{test_name}' completed with {attempt_count} attempts in {duration:.2f}s")
    else:
        print(f"📊 Test '{test_name}' completed in {duration:.2f}s")
    
    return final_result


def run_test_without_allure(test_path, test_name):
    """Run a specific test without generating Allure results."""
    print(f"Running: {test_name}")
    
    cmd = [
        sys.executable, "-m", "pytest", 
        test_path, 
        "-v", "-s", 
        "--tb=short"
    ]
    
    # Set PYTHONPATH
    env = os.environ.copy()
    env['PYTHONPATH'] = os.getcwd()
    
    result = subprocess.run(cmd, env=env)
    return result.returncode
