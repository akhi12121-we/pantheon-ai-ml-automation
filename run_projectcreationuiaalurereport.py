#!/usr/bin/env python3
"""
Script to run UI test cases for project creation, scheduling, and searching with Allure reporting.
"""
import sys
import os
import time
import subprocess
from utils.allure_helper import allure_helper
from generate_allure_html import generate_allure_html, serve_allure_report

def run_single_test(test_path, test_name):
    """Run a single test file and generate Allure result."""
    print(f"Running: {test_path}")
    start_time = time.time()
    
    result = subprocess.run([sys.executable, "-m", "pytest", test_path, "-v"], 
                          capture_output=True, text=True)
    
    end_time = time.time()
    status = "passed" if result.returncode == 0 else "failed"
    
    # Generate Allure result for this test
    test_uuid = allure_helper.generate_test_result(
        test_name=test_name,
        status=status,
        start_time=start_time,
        end_time=end_time,
        log_file=f"logs/automation_{time.strftime('%Y%m%d')}.log"
    )
    
    print(f"Test result: {'PASSED' if result.returncode == 0 else 'FAILED'}")
    return result.returncode

def run_test_with_retry(test_path, test_name, max_retries=3, delay_seconds=30):
    """Run a test with retry logic and generate single Allure result."""
    print(f"Running: {test_path}")
    overall_start_time = time.time()
    attempt_count = 0
    
    for attempt in range(1, max_retries + 1):
        attempt_count = attempt
        print(f"Attempt {attempt}/{max_retries}: {test_path}")
        
        result = subprocess.run([sys.executable, "-m", "pytest", test_path, "-v"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Test passed on attempt {attempt}")
            break
        else:
            print(f"❌ Test failed on attempt {attempt}")
            if attempt < max_retries:
                print(f"⏳ Waiting {delay_seconds} seconds before retry...")
                time.sleep(delay_seconds)
    
    overall_end_time = time.time()
    final_status = "passed" if result.returncode == 0 else "failed"
    
    # Generate single Allure result for the entire test (with retries)
    allure_test_name = test_name
    if attempt_count > 1:
        allure_test_name = f"{test_name} (Attempts: {attempt_count}/{max_retries})"
    
    test_uuid = allure_helper.generate_test_result(
        test_name=allure_test_name,
        status=final_status,
        start_time=overall_start_time,
        end_time=overall_end_time,
        log_file=f"logs/automation_{time.strftime('%Y%m%d')}.log",
        retry_count=attempt_count if attempt_count > 1 else 0
    )
    
    if result.returncode != 0:
        print(f"❌ Test failed after {max_retries} attempts")
    
    return result.returncode

def main():
    """Run UI tests in the correct order with Allure reporting."""
    print("Starting UI Project Creation Workflow with Allure Reporting")
    print("=" * 70)
    
    # Clean old Allure results using existing helper
    print("🧹 Cleaning old Allure results...")
    allure_helper.clean_results()
    
    # Test 1: Create XTM Project (UI) - 3 retries if fail
    print("\n🚀 Test 1: Create XTM Project (UI)")
    result1 = run_test_with_retry("tests/ui/test_xtm_ProjectCreation.py", "Create XTM Project (UI)", 3, 30)
    if result1 != 0:
        print("❌ XTM Project creation failed, but continuing...")
    
    # Test 2: Create Scheduler Job (UI) - 3 retries if fail
    print("\n🚀 Test 2: Create Scheduler Job (UI)")
    result2 = run_test_with_retry("tests/ui/test_createScheduler.py", "Create Scheduler Job (UI)", 3, 30)
    if result2 != 0:
        print("❌ Scheduler creation failed, but continuing...")
    
    # Test 3: Search Project (UI) - 3 retries if fail
    print("\n🚀 Test 3: Search Project (UI)")
    result3 = run_test_with_retry("tests/ui/test_SearchProjectRelay.py", "Search Project (UI)", 3, 30)
    if result3 != 0:
        print("❌ Project search failed, but continuing...")
    
    # Wait for 3 minutes
    print("\n⏳ Waiting for 3 minutes...")
    time.sleep(180)  # 3 minutes wait
    
    # Test 4: Verify Pulled Project Production Status (UI) - 3 retries with 3 min delay
    print("\n🚀 Test 4: Verify Pulled Project Production Status (UI)")
    result4 = run_test_with_retry("tests/ui/test_PulledProjectWithStatusProduction.py", "Verify Pulled Project Production Status (UI)", 3, 180)  # 3 min delay
    
    # Check if production status test failed - if so, skip remaining tests
    if result4 != 0:
        print("❌ Production status verification failed - skipping remaining tests")
        print("⏭️ Skipping remaining tests due to production status failure")
        
        # Generate skipped test results for remaining tests
        skipped_tests = [
            "AI Task Verification (UI)",
            "Project Search and Segment Navigation (UI)", 
            "Verify MT Copy Edit Count with Quote MT (UI)"
        ]
        
        for test_name in skipped_tests:
            allure_helper.generate_test_result(
                test_name=test_name,
                status="skipped",
                log_file=f"logs/automation_{time.strftime('%Y%m%d')}.log"
            )
            print(f"⏭️ Skipped {test_name} due to production status failure")
        
        print("\n" + "="*70)
        print("❌ UI Project Creation Tests Completed with Failures!")
        print("="*70)
        
        # Generate Allure HTML report using existing helper
        print("📊 Generating Allure HTML Report...")
        generate_allure_html()
        return 1
    
    # Wait for 10 minutes
    print("\n⏳ Waiting for 10 minutes...")
    time.sleep(600)  # 10 minutes wait
    
    # Test 5: AI Task Verification (UI) - 3 retries with 10 min delay
    print("\n🚀 Test 5: AI Task Verification (UI)")
    result5 = run_test_with_retry("tests/ui/test_verifyAITaskVerification.py", "AI Task Verification (UI)", 3, 600)  # 10 min delay
    if result5 != 0:
        print("❌ AI Task verification failed, but continuing...")
    
    # Wait for 1 minute
    print("\n⏳ Waiting for 1 minute...")
    time.sleep(60)  # 1 minute wait
    
    # Test 6: Project Search and Segment Navigation (UI) - 3 retries
    print("\n🚀 Test 6: Project Search and Segment Navigation (UI)")
    result6 = run_test_with_retry("tests/ui/test_xtmProjectSearchClicktoSegments.py", "Project Search and Segment Navigation (UI)", 3, 30)
    if result6 != 0:
        print("❌ Project search and segment navigation failed, but continuing...")
    
    # Test 7: Verify MT Copy Edit Count with Quote MT - 3 retries
    print("\n🚀 Test 7: Verify MT Copy Edit Count with Quote MT")
    result7 = run_test_with_retry("tests/ui/test_verifyMTCopyEditCount_with_QuoteMT.py", "Verify MT Copy Edit Count with Quote MT (UI)", 3, 30)
    if result7 != 0:
        print("❌ MT Copy Edit Count verification failed, but continuing...")
    
    print("\n" + "="*70)
    print("✅ All UI Project Creation Tests Completed!")
    print("="*70)
    
    # Generate Allure HTML report using existing helper
    print("📊 Generating Allure HTML Report...")
    generate_allure_html()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
