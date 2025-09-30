#!/usr/bin/env python3
"""
Script to run UI test cases for project creation, scheduling, and searching.
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
    return result.returncode

def main():
    """Run UI tests in the correct order."""
    print("Starting UI Project Creation Workflow")
    print("=" * 60)
    
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
    
    print("\n" + "="*60)
    print("✅ All UI Project Creation Tests Completed Successfully!")
    print("="*60)
    return 0

if __name__ == "__main__":
    sys.exit(main())
