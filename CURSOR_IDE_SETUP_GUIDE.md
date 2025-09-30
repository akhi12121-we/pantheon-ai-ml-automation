# Backend Automation Framework - Cursor IDE Setup Guide

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Cursor IDE Configuration](#cursor-ide-configuration)
4. [Python Environment Setup](#python-environment-setup)
5. [Framework Configuration](#framework-configuration)
6. [Test Execution](#test-execution)
7. [Allure Reporting](#allure-reporting)
8. [Troubleshooting](#troubleshooting)
9. [Best Practices](#best-practices)

---

## 🎯 Prerequisites

### Required Software
- **Cursor IDE** (Latest version)
- **Python 3.9+** (Recommended: Python 3.11 or 3.12)
- **Java JDK 8+** (For Allure reports)
- **Git** (For version control)

### System Requirements
- **Windows 10/11** (Primary support)
- **macOS** (Secondary support)
- **Linux** (Basic support)
- **Minimum 8GB RAM**
- **10GB free disk space**

---

## 🚀 Initial Setup

### Step 1: Clone the Repository
```bash
# Clone the automation framework
git clone <repository-url>
cd backendAutomationFramework

# Verify the project structure
ls -la
```

### Step 2: Install Python Dependencies
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Verify Installation
```bash
# Check Python version
python --version

# Check installed packages
pip list

# Verify pytest installation
pytest --version
```

---

## ⚙️ Cursor IDE Configuration

### Step 1: Open Project in Cursor IDE
1. Launch **Cursor IDE**
2. Click **File** → **Open Folder**
3. Navigate to `backendAutomationFramework` directory
4. Click **Select Folder**

### Step 2: Install Required Extensions
1. Open **Extensions** panel (`Ctrl+Shift+X`)
2. Install the following extensions:

#### Essential Extensions:
- **Python** (by Microsoft)
- **Pytest** (by Little Fox Team)
- **Python Test Explorer** (by Little Fox Team)
- **Allure** (by Qameta Software)
- **GitLens** (by Eric Amodio)

#### Optional Extensions:
- **Python Docstring Generator** (by Nils Werner)
- **autoDocstring** (by Nils Werner)
- **Python Indent** (by Kevin Rose)
- **Python Type Hint** (by njqdev)

### Step 3: Configure Python Interpreter
1. Press `Ctrl+Shift+P` to open command palette
2. Type "Python: Select Interpreter"
3. Select the virtual environment interpreter:
   ```
   .venv\Scripts\python.exe (Windows)
   .venv/bin/python (macOS/Linux)
   ```

### Step 4: Configure Workspace Settings
1. Press `Ctrl+Shift+P`
2. Type "Preferences: Open Workspace Settings (JSON)"
3. Add the following configuration:

```json
{
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.testing.pytestArgs": [
        "-s",
        "--capture=no",
        "--tb=short",
        "--log-cli-level=INFO",
        "--log-cli-format=%(asctime)s [%(levelname)8s] %(name)s: %(message)s",
        "--log-cli-date-format=%Y-%m-%d %H:%M:%S"
    ],
    "python.testing.autoTestDiscoverOnSaveEnabled": true,
    "python.testing.cwd": "${workspaceFolder}",
    "python.terminal.activateEnvironment": true,
    "python.terminal.executeInFileDir": false,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.testing.outputConfig": {
        "openTesting": "neverOpen",
        "revealTestOutputOn": "run"
    },
    "python.testing.showOutput": true,
    "python.testing.verboseOutput": true,
    "terminal.integrated.env.windows": {
        "PYTHONPATH": "${workspaceFolder}"
    },
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        "**/node_modules": true,
        "**/.pytest_cache": true
    }
}
```

---

## 🐍 Python Environment Setup

### Step 1: Verify Virtual Environment
```bash
# Check if virtual environment is active
echo $VIRTUAL_ENV  # Should show path to .venv

# Check Python path
which python  # Should point to .venv/bin/python
```

### Step 2: Install Framework Dependencies
```bash
# Install core dependencies
pip install pytest pytest-html pytest-cov pytest-asyncio
pip install allure-pytest allure-python-commons
pip install playwright requests python-dotenv
pip install black flake8

# Install Playwright browsers
playwright install
```

### Step 3: Verify Environment Variables
Create a `.env` file in the project root:
```bash
# API Configuration
APOLLO_URL=https://apollo.welocalize.io
AIQE_URL=https://aiqe-api.example.com
APIE_URL=https://apie-api.example.com

# UI Configuration
BASE_URL=https://apollo.welocalize.io
BROWSER_TYPE=chromium
HEADLESS=true

# Test Configuration
LOG_LEVEL=INFO
SCREENSHOT_ON_FAILURE=true
VIDEO_RECORDING=false
```

---

## 🔧 Framework Configuration

### Step 1: Configure pytest.ini
The framework includes a pre-configured `pytest.ini` file:

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose 
    -s
    --capture=no
    --tb=short
    --html=reports/report.html
    --self-contained-html
    --cov=utils
    --cov=config
    --cov-report=html:reports/coverage
    --cov-report=term-missing
    --junitxml=reports/junit.xml
    # --alluredir=allure-results  # Temporarily disabled due to Python 3.13 compatibility issue
markers =
    smoke: Smoke tests
    regression: Regression tests
    api: API tests
    ui: UI tests
    hybrid: Hybrid tests
    slow: Slow tests
asyncio_mode = auto
```

### Step 2: Configure Allure (Optional)
```bash
# Download Allure (if not already included)
# The framework includes Allure 2.24.1 in the allure/ directory

# Verify Allure installation
allure/allure-2.24.1/bin/allure.bat --version
```

---

## 🧪 Test Execution

### Method 1: Using Cursor IDE Test Explorer
1. Open **Test Explorer** panel (`Ctrl+Shift+T`)
2. Wait for tests to be discovered
3. Click the **Run** button next to individual tests or test suites
4. View results in the **Test Results** panel

### Method 2: Using Command Palette
1. Press `Ctrl+Shift+P`
2. Type "Python: Run All Tests"
3. Or type "Python: Run Current Test" for individual tests

### Method 3: Using Terminal
```bash
# Run all tests
pytest tests/ -v -s

# Run specific test file
pytest tests/api/test_apollo/test_apollo.py -v -s

# Run specific test method
pytest tests/api/test_apollo/test_apollo.py::TestApollo::test_health_check -v -s

# Run UI tests
pytest tests/ui/test_simple_ui.py -v -s

# Run with markers
pytest -m smoke -v -s
pytest -m "not slow" -v -s
```

### Method 4: Using Framework Scripts
```bash
# Run tests and generate Allure report
python generate_allure_html.py run

# Run specific test path
python generate_allure_html.py run tests/ui/test_simple_ui.py

# Run API tests
python generate_allure_html.py run tests/api/test_apollo/
```

---

## 📊 Allure Reporting

### Step 1: Generate Allure Results
The framework automatically generates Allure results when tests run.

### Step 2: View Allure Reports
```bash
# Method 1: Generate and serve report (Recommended)
python generate_allure_html.py run tests/ui/test_simple_ui.py

# Method 2: Generate report from existing results
python generate_allure_html.py generate-serve

# Method 3: Serve existing report
python generate_allure_html.py serve
```

### Step 3: Access Report
- The report will open automatically in your browser
- URL format: `http://localhost:port`
- All sections (Overview, Suites, Categories) will work properly

---

## 🔍 Troubleshooting

### Common Issues and Solutions

#### Issue 1: Tests Not Discovered
**Problem**: Test Explorer shows no tests
**Solution**:
```bash
# Reload window
Ctrl+Shift+P → "Developer: Reload Window"

# Check Python interpreter
Ctrl+Shift+P → "Python: Select Interpreter"

# Verify pytest installation
pip install pytest pytest-asyncio
```

#### Issue 2: Import Errors
**Problem**: ModuleNotFoundError when running tests
**Solution**:
```bash
# Add project root to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or add to .vscode/settings.json
"terminal.integrated.env.windows": {
    "PYTHONPATH": "${workspaceFolder}"
}
```

#### Issue 3: Allure Plugin Errors
**Problem**: `'str' object has no attribute 'iter_parents'`
**Solution**:
- This is a known compatibility issue with Python 3.13
- The framework uses a custom Allure helper to work around this
- No action needed - it's already configured

#### Issue 4: Print Statements Not Visible
**Problem**: Print statements don't show in Cursor IDE test output
**Solution**:
- The framework includes enhanced logging with forced output
- Use `logger.info()` instead of `print()`
- Or use `ide_output.force_print()` for guaranteed visibility

#### Issue 5: Browser Tests Not Working
**Problem**: Playwright tests fail to start browser
**Solution**:
```bash
# Install Playwright browsers
playwright install

# Check browser configuration in config/settings.py
# Ensure BROWSER_TYPE and HEADLESS settings are correct
```

#### Issue 6: Allure Report 404 Errors
**Problem**: Allure report shows 404 errors when opened directly
**Solution**:
- Always use the serve functionality: `python generate_allure_html.py serve`
- Never open the HTML file directly in browser
- Use the provided commands for proper report viewing

---

## 📝 Best Practices

### 1. Test Organization
- Keep API tests in `tests/api/`
- Keep UI tests in `tests/ui/`
- Use descriptive test names
- Group related tests in classes

### 2. Configuration Management
- Use environment variables for different environments
- Keep sensitive data in `.env` file (not committed)
- Use `config/settings.py` for framework configuration

### 3. Reporting
- Always use the serve functionality for Allure reports
- Clean old results before generating new reports
- Use appropriate test markers for categorization

### 4. Code Quality
- Use type hints in Python code
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes

### 5. Debugging
- Use the enhanced logger for consistent output
- Take screenshots on test failures
- Use the IDE output helper for guaranteed visibility
- Check logs in the `logs/` directory

---

## 🎯 Quick Start Checklist

- [ ] Clone repository
- [ ] Create and activate virtual environment
- [ ] Install dependencies (`pip install -r requirements.txt`)
- [ ] Open project in Cursor IDE
- [ ] Install required extensions
- [ ] Configure Python interpreter
- [ ] Update workspace settings
- [ ] Create `.env` file with configuration
- [ ] Run a test to verify setup
- [ ] Generate and view Allure report

---

## 📞 Support

For additional help:
1. Check the `README.md` file in the project root
2. Review the troubleshooting section above
3. Check the logs in the `logs/` directory
4. Contact the automation team

---

## 🔄 Updates

This guide is updated regularly. Last updated: September 2025

For the latest version, always refer to the project repository.
