#!/usr/bin/env python3
"""
Script to run OpalInternalFlowAPI tests in the correct order using pytest.
"""
import pytest
import sys
import os
import time
from utils.allure_helper import allure_helper
from generate_allure_html import generate_allure_html

def run_test_with_pytest(test_path, test_name):
    """Run a specific test using pytest directly."""
    print(f"\n{'='*60}")
    print(f"Running: {test_name}")
    print(f"{'='*60}")

    # Set PYTHONPATH
    os.environ['PYTHONPATH'] = os.getcwd()

    # Create log file for this specific test
    log_file = f"logs/{test_name.replace(' ', '_').lower()}_{int(time.time())}.log"
    os.makedirs("logs", exist_ok=True)

    # Run pytest with specific test path and logging
    pytest_args = [
        test_path,
        "-v", "-s",
        "--tb=short",
        f"--log-file={log_file}",
        "--log-file-level=INFO",
        "--log-file-format=%(asctime)s [%(levelname)8s] %(name)s: %(message)s",
        "--log-file-date-format=%Y-%m-%d %H:%M:%S"
    ]

    # Run pytest and capture exit code
    exit_code = pytest.main(pytest_args)

    # Generate Allure result for this test with log file
    try:
        status = "passed" if exit_code == 0 else "failed"
        allure_helper.generate_test_result(
            test_name=test_name,
            status=status,
            test_class="OpalInternalFlowAPI",
            package="tests.api.OpalInternalFlowAPI",
            suite="Opal Internal Flow API Tests",
            log_file=log_file
        )
    except Exception as e:
        print(f"⚠️ Could not generate Allure result: {e}")

    return exit_code

def main():
    """Run tests in the correct order."""
    print("Starting Opal Internal Flow API Test Workflow")
    print("=" * 60)
    
    # Clean old Allure results
    print("🧹 Cleaning old Allure results...")
    try:
        allure_helper.clean_results()
    except Exception as e:
        print(f"⚠️ Could not clean old results: {e}")
    
    # Test sequence as requested
    tests = [
        {
            "path": "tests/api/OpalInternalFlowAPI/test_tokenGenerated.py",
            "name": "Generate Token"
        },
        {
            "path": "tests/api/OpalInternalFlowAPI/test_verifyGeneratedTokenGetCall.py", 
            "name": "Verify Generated Token Get Call"
        },
        {
            "path": "tests/api/OpalInternalFlowAPI/test_createProjectopalpost.py",
            "name": "Create Project"
        },
        {
            "path": "tests/api/OpalInternalFlowAPI/test_ProjectFileUpload.py",
            "name": "Upload File"
        },
        {
            "path": "tests/api/OpalInternalFlowAPI/test_projectMultiFileUpload.py",
            "name": "Multi Upload"
        },
        {
            "path": "tests/api/OpalInternalFlowAPI/test_verifyProjectGetDetailsBeforeComplete.py",
            "name": "Get Project Details Before Complete"
        },
        {
            "path": "tests/api/OpalInternalFlowAPI/test_ProjectStart.py",
            "name": "Start Project"
        },
        {
            "path": "tests/api/OpalInternalFlowAPI/test_ProjectComplete.py",
            "name": "Complete Project"
        },
        {
            "path": "tests/api/OpalInternalFlowAPI/test_verifyProjectGetDetailsAfterComplete.py",
            "name": "Get Project Details After Complete"
        }
    ]
    
    failed_tests = []
    
    for i, test in enumerate(tests, 1):
        print(f"\n{i}. {test['name']}")
        result = run_test_with_pytest(test['path'], test['name'])
        
        if result != 0:
            print(f"❌ {test['name']} failed!")
            failed_tests.append(test['name'])
            # Continue with next test instead of stopping
            print("⚠️ Continuing with next test...")
        else:
            print(f"✅ {test['name']} passed!")
    
    print("\n" + "="*60)
    if failed_tests:
        print(f"⚠️ Test Workflow Completed with {len(failed_tests)} failures:")
        for test in failed_tests:
            print(f"   - {test}")
    else:
        print("✅ All Opal Internal Flow API Tests Completed Successfully!")
    print("="*60)
    
    # Generate Allure Report
    print("\n📊 Generating Allure Report...")
    try:
        generate_allure_html()
        print("✅ Allure report generated successfully!")
        print("🌐 Open allure-report/index.html to view the report")
    except Exception as e:
        print(f"❌ Failed to generate Allure report: {e}")
    
    return 0 if not failed_tests else 1

if __name__ == "__main__":
    sys.exit(main())
