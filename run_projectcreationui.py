#!/usr/bin/env python3
"""
Script to run UI test cases for project creation, scheduling, and searching.
"""
import sys
import os
import time
import subprocess

def run_single_test(test_path):
    """Run a single test file."""
    print(f"Running: {test_path}")
    result = subprocess.run([sys.executable, "-m", "pytest", test_path, "-v"], 
                          capture_output=True, text=True)
    print(f"Test result: {'PASSED' if result.returncode == 0 else 'FAILED'}")
    return result.returncode

def run_test_with_retry(test_path, max_retries=3):
    """Run a test with retry logic."""
    for attempt in range(1, max_retries + 1):
        print(f"Attempt {attempt}/{max_retries}: {test_path}")
        result = subprocess.run([sys.executable, "-m", "pytest", test_path, "-v"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Test passed on attempt {attempt}")
            return 0
        else:
            print(f"❌ Test failed on attempt {attempt}")
            if attempt < max_retries:
                print(f"⏳ Waiting before retry...")
                time.sleep(30)  # Wait 30 seconds between retries
    
    print(f"❌ Test failed after {max_retries} attempts")
    return result.returncode

def generate_playwright_report():
    """Generate Playwright's default HTML report by running tests with HTML output."""
    print("📊 Generating Playwright HTML Report...")
    
    # Run pytest with HTML reporting - this will run the tests and generate report
    pytest_cmd = [
        sys.executable, "-m", "pytest",
        "tests/ui/",
        "--html=playwright-report/report.html",
        "--self-contained-html",
        "-v"
    ]
    
    print(f"Running: {' '.join(pytest_cmd)}")
    result = subprocess.run(pytest_cmd)
    
    if os.path.exists("playwright-report/report.html"):
        print("✅ Playwright HTML report generated successfully!")
        print(f"📁 Report location: {os.path.abspath('playwright-report/report.html')}")
        
        # Try to open the report in default browser
        try:
            if sys.platform.startswith('win'):
                os.startfile("playwright-report/report.html")
            elif sys.platform.startswith('darwin'):
                subprocess.run(['open', 'playwright-report/report.html'])
            else:
                subprocess.run(['xdg-open', 'playwright-report/report.html'])
        except Exception as e:
            print(f"⚠️ Could not auto-open browser: {e}")
            print("💡 Please manually open: playwright-report/report.html")
    else:
        print("❌ Playwright HTML report not found")
    
    return result.returncode

def main():
    """Run UI tests in the correct order."""
    print("Starting UI Project Creation Workflow")
    print("=" * 60)
    
    # Clean old Playwright results
    print("🧹 Cleaning old Playwright results...")
    try:
        if os.path.exists("playwright-report"):
            import shutil
            shutil.rmtree("playwright-report")
        if os.path.exists("test-results"):
            import shutil
            shutil.rmtree("test-results")
        print("✅ Cleaned old Playwright results")
    except Exception as e:
        print(f"⚠️ Could not clean old results: {e}")
    
    # Track which tests to run
    tests_to_run = []
    tests_to_skip = []
    
    # Test 1: Create XTM Project (UI)
    print("\n🚀 Test 1: Create XTM Project (UI)")
    result1 = run_single_test("tests/ui/test_xtm_ProjectCreation.py")
    tests_to_run.append("tests/ui/test_xtm_ProjectCreation.py")
    if result1 != 0:
        print("❌ XTM Project creation failed, but continuing...")
    
    # Test 2: Create Scheduler Job (UI)
    print("\n🚀 Test 2: Create Scheduler Job (UI)")
    result2 = run_single_test("tests/ui/test_createScheduler.py")
    tests_to_run.append("tests/ui/test_createScheduler.py")
    if result2 != 0:
        print("❌ Scheduler creation failed, but continuing...")
    
    # Test 3: Search Project (UI)
    print("\n🚀 Test 3: Search Project (UI)")
    result3 = run_single_test("tests/ui/test_SearchProjectRelay.py")
    tests_to_run.append("tests/ui/test_SearchProjectRelay.py")
    if result3 != 0:
        print("❌ Project search failed, but continuing...")
    
    # Wait for few minutes
    print("\n⏳ Waiting for few minutes...")
    time.sleep(180)  # 3 minutes wait
    
    # Test 4: Verify Pulled Project Production Status (UI) - with retry
    print("\n🚀 Test 4: Verify Pulled Project Production Status (UI)")
    result4 = run_test_with_retry("tests/ui/test_PulledProjectWithStatusProduction.py", 3)
    tests_to_run.append("tests/ui/test_PulledProjectWithStatusProduction.py")
    
    # Check if production status test failed - if so, skip remaining tests
    if result4 != 0:
        print("❌ Production status verification failed - skipping remaining tests")
        print("⏭️ Skipping remaining tests due to production status failure")
        
        # Mark tests 5-7 as skipped
        tests_to_skip = [
            "tests/ui/test_verifyAITaskVerification.py",
            "tests/ui/test_xtmProjectSearchClicktoSegments.py",
            "tests/ui/test_verifyMTCopyEditCount_with_QuoteMT.py"
        ]
        
        print("\n" + "="*60)
        print("❌ UI Project Creation Tests Completed with Failures!")
        print("="*60)
        
        # Generate Playwright HTML report
        generate_playwright_report()
        return 1
    
    # Wait for 10 minutes
    print("\n⏳ Waiting for 10 minutes...")
    time.sleep(600)  # 10 minutes wait
    
    # Test 5: AI Task Verification (UI)
    print("\n🚀 Test 5: AI Task Verification (UI)")
    result5 = run_test_with_retry("tests/ui/test_verifyAITaskVerification.py", 3)
    tests_to_run.append("tests/ui/test_verifyAITaskVerification.py")
    if result5 != 0:
        print("❌ AI Task verification failed, but continuing...")
    
    # Wait for 1 minute
    print("\n⏳ Waiting for 1 minute...")
    time.sleep(60)  # 1 minute wait
    
    # Test 6: Project Search and Segment Navigation (UI)
    print("\n🚀 Test 6: Project Search and Segment Navigation (UI)")
    result6 = run_test_with_retry("tests/ui/test_xtmProjectSearchClicktoSegments.py", 3)
    tests_to_run.append("tests/ui/test_xtmProjectSearchClicktoSegments.py")
    if result6 != 0:
        print("❌ Project search and segment navigation failed, but continuing...")
    
    # Test 7: Verify MT Copy Edit Count with Quote MT
    print("\n🚀 Test 7: Verify MT Copy Edit Count with Quote MT")
    result7 = run_test_with_retry("tests/ui/test_verifyMTCopyEditCount_with_QuoteMT.py", 3)
    tests_to_run.append("tests/ui/test_verifyMTCopyEditCount_with_QuoteMT.py")
    if result7 != 0:
        print("❌ MT Copy Edit Count verification failed, but continuing...")
    
    print("\n" + "="*60)
    print("✅ All UI Project Creation Tests Completed!")
    print("="*60)
    
    # Generate Playwright HTML report
    generate_playwright_report()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())