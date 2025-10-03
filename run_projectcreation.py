#!/usr/bin/env python3
"""
Script to run project creation tests in the correct order.
"""
import subprocess
import sys
import os

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
    
    result = subprocess.run(cmd, env=env)
    
    # Generate Allure result for this test
    try:
        from utils.allure_helper import allure_helper
        status = "passed" if result.returncode == 0 else "failed"
        allure_helper.generate_test_result(
            test_name=test_name,
            status=status,
            test_class="TestSuite",
            package="tests",
            suite="Project Creation Tests"
        )
    except Exception as e:
        print(f"⚠️ Could not generate Allure result: {e}")
    
    return result.returncode

def main():
    """Run tests in the correct order."""
    print("Starting Project Creation Workflow")
    print("=" * 60)
    
    # Clean old Allure results
    print("🧹 Cleaning old Allure results...")
    try:
        from utils.allure_helper import allure_helper
        allure_helper.clean_results()
    except Exception as e:
        print(f"⚠️ Could not clean old results: {e}")
    
    # Test 1: Create Project (UI)
    print("\n1. Creating Project (UI Test)")
    result1 = run_test(
        "tests/ui/test_xtm_ProjectCreation.py::test_01_create_xtm_project",
        "Create XTM Project"
    )
    
    if result1 != 0:
        print("❌ Project creation failed!")
        return result1
    
    # Test 2: Pull Project (API)
    print("\n2. Pulling Project (API Test)")
    result2 = run_test(
        "tests/api/test_pullProject/test_pullProjectScheduler.py::TestPullProjectScheduler::test_02_pull_project_trigger_job",
        "Pull Project Scheduler"
    )
    
    if result2 != 0:
        print("❌ Project pull failed!")
        return result2
    
    # Test 3: Search Project (API)
    print("\n3. Searching Project (API Test)")
    result3 = run_test(
        "tests/api/fetchProjectAndTask/03-test_ProjectSearchAPI.py::TestProjectSearchAPI::test_03_project_search_api",
        "Project Search API"
    )
    
    if result3 != 0:
        print("❌ Project search failed!")
        return result3
    
    print("\n" + "="*60)
    print("✅ All Project Creation Tests Completed Successfully!")
    print("="*60)
    
    # Generate Allure Report
    print("\n📊 Generating Allure Report...")
    try:
        from generate_allure_html import generate_allure_html
        generate_allure_html()
        print("✅ Allure report generated successfully!")
    except Exception as e:
        print(f"❌ Failed to generate Allure report: {e}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
