#!/usr/bin/env python3
"""
Script to run UI test cases for project creation, scheduling, and searching.
"""
import subprocess
import sys
import os
import time

def run_test(test_path, test_name):
    """Run a specific test."""
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
    import time
    test_start_time = time.time()
    
    result = subprocess.run(cmd, env=env)
    
    # Record test end time
    test_end_time = time.time()
    
    # Generate Allure result with real logger steps
    try:
        from utils.allure_helper import allure_helper
        from datetime import datetime
        
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

def main():
    """Run UI tests in the correct order."""
    print("Starting UI Project Creation Workflow")
    print("=" * 60)
    
    # Clean old Allure results
    print("🧹 Cleaning old Allure results...")
    try:
        from utils.allure_helper import allure_helper
        allure_helper.clean_results()
    except Exception as e:
        print(f"⚠️ Could not clean old results: {e}")
    
    # Test 1: Create XTM Project (UI)
    print("\n1. Creating XTM Project (UI Test)")
    result1 = run_test(
        "tests/ui/test_xtm_ProjectCreation.py",
        "Create XTM Project"
    )
    
    if result1 != 0:
        print("❌ XTM Project creation failed!")
        return result1
    
    # Test 2: Create Scheduler Job (UI)
    print("\n2. Creating Scheduler Job (UI Test)")
    result2 = run_test(
        "tests/ui/test_createScheduler.py",
        "Create Scheduler Job"
    )
    
    if result2 != 0:
        print("❌ Scheduler job creation failed!")
        return result2
    
    # Test 3: Search Project (UI)
    print("\n3. Searching Project (UI Test)")
    result3 = run_test(
        "tests/ui/test_SearchProjectRelay.py",
        "Search Project Relay"
    )
    
    if result3 != 0:
        print("❌ Project search failed!")
        return result3
    
    # Test 4: Verify Pulled Project Production Status (UI) - with retry
    print("\n4. Verifying Pulled Project Production Status (UI Test)")
    print("⏳ Waiting 2 minutes before running production status verification...")
    time.sleep(120)  # Wait 2 minutes
    
    # Retry logic for production status verification
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        print(f"\n🔄 Attempt {attempt}/{max_retries}: Verifying Production Status")
        result4 = run_test(
            "tests/ui/test_PulledProjectWithStatusProduction.py",
            "Verify Pulled Project Production Status"
        )
        
        if result4 == 0:
            print("✅ Production status verification successful!")
            break
        else:
            print(f"❌ Production status verification failed on attempt {attempt}")
            if attempt < max_retries:
                print(f"⏳ Waiting 5 minutes before retry {attempt + 1}...")
                time.sleep(300)  # Wait 5 minutes before retry
            else:
                print("❌ All retry attempts failed for production status verification!")
                return result4
    
    # Test 5: AI Task Verification - with retry
    print("\n5. Running AI Task Verification (UI Test)")
    print("⏳ Waiting 600 seconds before running AI task verification...")
    time.sleep(600)  # Wait 10 minutes
    
    # Retry logic for AI task verification
    max_retries = 5
    for attempt in range(1, max_retries + 1):
        print(f"\n🔄 Attempt {attempt}/{max_retries}: AI Task Verification")
        result5 = run_test(
            "tests/ui/test_verifyAITaskVerification.py",
            "Verify AI Task Completion"
        )
        
        if result5 == 0:
            print("✅ AI task verification successful!")
            break
        else:
            print(f"❌ AI task verification failed on attempt {attempt}")
            if attempt < max_retries:
                print(f"⏳ Waiting 10 minutes before retry {attempt + 1}...")
                time.sleep(180)  # Wait 10 minutes before retry
            else:
                print("❌ All retry attempts failed for AI task verification!")
                return result5
    
    print("\n" + "="*60)
    print("✅ All UI Project Creation Tests Completed Successfully!")
    print("="*60)
    
    # Generate Allure Report
    print("\n📊 Generating Allure Report...")
    try:
        from generate_allure_html import generate_allure_html, serve_allure_report
        if generate_allure_html():
            print("✅ Allure report generated successfully!")
            print("🌐 Starting Allure server...")
            print("💡 Press Ctrl+C to stop the server when done viewing the report.")
            serve_allure_report()
        else:
            print("❌ Failed to generate Allure report")
    except Exception as e:
        print(f"❌ Failed to generate Allure report: {e}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
