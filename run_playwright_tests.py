#!/usr/bin/env python3
"""
Simple script to run Playwright tests with HTML reporting.
"""
import sys
import os
import subprocess

def run_tests():
    """Run tests with Playwright HTML reporting."""
    print("🚀 Running Playwright Tests with HTML Report")
    print("=" * 50)
    
    # Command to run tests
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/ui/",
        "-v",
        "--html=playwright-report/report.html",
        "--self-contained-html",
        "--retries=3",
        "--tb=short"
    ]
    
    print("📋 Command:", " ".join(cmd))
    print("=" * 50)
    
    # Run tests
    result = subprocess.run(cmd, env=os.environ.copy())
    
    # Check if report was generated
    if os.path.exists("playwright-report/report.html"):
        print("\n✅ HTML Report generated successfully!")
        print(f"📁 Report location: {os.path.abspath('playwright-report/report.html')}")
        
        # Try to open in browser
        try:
            if sys.platform.startswith('win'):
                os.startfile("playwright-report/report.html")
            elif sys.platform.startswith('darwin'):
                subprocess.run(['open', 'playwright-report/report.html'])
            else:
                subprocess.run(['xdg-open', 'playwright-report/report.html'])
        except Exception as e:
            print(f"⚠️ Could not auto-open browser: {e}")
    else:
        print("❌ HTML Report not found")
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(run_tests())
