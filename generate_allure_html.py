#!/usr/bin/env python3
"""
Generate Allure HTML report from JSON results.
"""
import os
import subprocess
import sys
from pathlib import Path

def clean_allure_results():
    """Clean all existing Allure results."""
    from utils.allure_helper import allure_helper
    allure_helper.clean_results()
    return True

def fix_allure_results():
    """Fix existing Allure results to make them compatible."""
    import json
    import os
    from pathlib import Path
    
    results_dir = Path("allure-results")
    if not results_dir.exists():
        print("❌ No Allure results found to fix.")
        return False
    
    print("🔧 Fixing Allure results...")
    
    # Find all result files
    result_files = list(results_dir.glob("*-result.json"))
    if not result_files:
        print("❌ No result files found.")
        return False
    
    # Create containers for each result
    containers_created = 0
    for result_file in result_files:
        try:
            with open(result_file, 'r', encoding='utf-8') as f:
                result_data = json.load(f)
            
            # Create container file
            container_uuid = str(result_data['uuid']).replace('-result', '-container')
            container_data = {
                "uuid": container_uuid,
                "name": result_data.get('name', 'Test'),
                "children": [result_data['uuid']],
                "befores": [],
                "afters": []
            }
            
            container_file = results_dir / f"{container_uuid}.json"
            with open(container_file, 'w', encoding='utf-8') as f:
                json.dump(container_data, f, indent=2)
            
            containers_created += 1
            
        except Exception as e:
            print(f"⚠️ Error fixing {result_file}: {e}")
            continue
    
    print(f"✅ Fixed {containers_created} result files with containers.")
    return True

def generate_allure_html(clean_first: bool = False):
    """Generate Allure HTML report."""
    allure_bin = Path("allure/allure-2.24.1/bin/allure.bat")
    allure_results = Path("allure-results")
    output_dir = Path("allure-report")
    
    # Clean results first if requested
    if clean_first:
        clean_allure_results()
    
    # Check if Allure is installed
    if not allure_bin.exists():
        print("❌ Allure not found. Please install Allure first.")
        print("💡 Download from: https://github.com/allure-framework/allure2/releases")
        return False
    
    # Check if results exist
    if not allure_results.exists():
        print("❌ No Allure results found. Run tests first to generate results.")
        print("💡 Use: pytest tests/ -v -s")
        return False
    
    # Fix existing results to make them compatible
    print("🔧 Fixing Allure results for compatibility...")
    fix_allure_results()
    
    print("🎭 Generating Allure HTML report...")
    
    try:
        # Generate HTML report
        cmd = [str(allure_bin), "generate", str(allure_results), "--clean", "--output", str(output_dir)]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        print("✅ Allure HTML report generated successfully!")
        print(f"📁 Report location: {output_dir.absolute()}")
        print(f"🌐 Open: {output_dir}/index.html")
        
        # Note: Allure reports need to be served through a web server to work properly
        # Opening the HTML file directly causes 404 errors due to CORS restrictions
        print("💡 Note: Allure reports work best when served through a web server.")
        print("💡 Use 'python generate_allure_html.py serve' to view the report properly.")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error generating report: {e}")
        print(f"Error output: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def run_tests_and_generate_report(test_path: str = "tests/", clean_results: bool = True):
    """Run tests and generate Allure report in one command."""
    print("🧪 Running tests...")
    
    # Clean old results if requested
    if clean_results:
        from utils.allure_helper import allure_helper
        allure_helper.clean_results()
    
    try:
        # Run pytest with proper Allure integration
        cmd = ["pytest", test_path, "-v", "-s", "--alluredir=allure-results"]
        result = subprocess.run(cmd, check=True)
        
        print("✅ Tests completed successfully!")
        
        # Generate HTML report
        if generate_allure_html():
            print("\n🌐 Starting Allure server to view the report...")
            print("💡 The report will open in your browser automatically.")
            print("💡 Press Ctrl+C to stop the server when you're done viewing the report.")
            serve_allure_report()
            return True
        else:
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Tests failed: {e}")
        # Even if tests fail, try to generate report from existing results
        print("🔄 Attempting to generate report from existing results...")
        if generate_allure_html():
            serve_allure_report()
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def serve_allure_report():
    """Serve Allure report on local server."""
    allure_bin = Path("allure/allure-2.24.1/bin/allure.bat")
    allure_results = Path("allure-results")
    
    if not allure_bin.exists():
        print("❌ Allure not found. Please install Allure first.")
        return False
    
    if not allure_results.exists():
        print("❌ No Allure results found. Run tests first to generate results.")
        print("💡 Use: pytest tests/ -v -s")
        return False
    
    print("🌐 Starting Allure server...")
    print("💡 Press Ctrl+C to stop the server")
    
    try:
        cmd = [str(allure_bin), "serve", str(allure_results)]
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped.")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "serve":
            serve_allure_report()
        elif sys.argv[1] == "run":
            test_path = sys.argv[2] if len(sys.argv) > 2 else "tests/"
            clean_results = "--no-clean" not in sys.argv
            run_tests_and_generate_report(test_path, clean_results)
        elif sys.argv[1] == "clean":
            clean_allure_results()
        elif sys.argv[1] == "fix":
            fix_allure_results()
        elif sys.argv[1] == "generate":
            clean_first = "--clean" in sys.argv
            generate_allure_html(clean_first)
        elif sys.argv[1] == "generate-serve":
            clean_first = "--clean" in sys.argv
            if generate_allure_html(clean_first):
                print("\n🌐 Starting Allure server to view the report...")
                serve_allure_report()
        else:
            print("Usage:")
            print("  python generate_allure_html.py                    # Generate report from existing results")
            print("  python generate_allure_html.py --clean            # Clean results and generate report")
            print("  python generate_allure_html.py serve              # Serve report on local server")
            print("  python generate_allure_html.py generate-serve     # Generate and serve report (recommended)")
            print("  python generate_allure_html.py run                # Run tests, generate and serve report")
            print("  python generate_allure_html.py run --no-clean     # Run tests and generate report (keeps old results)")
            print("  python generate_allure_html.py run tests/ui/      # Run specific test path")
            print("  python generate_allure_html.py clean              # Clean all Allure results")
            print("  python generate_allure_html.py fix                # Fix existing results for compatibility")
    else:
        generate_allure_html()
