# 🚀 Python Playwright Hybrid Automation Framework

A comprehensive **Hybrid API + UI Automation Framework** built with Python, Playwright, and pytest. This framework provides a unified solution for testing both backend APIs and frontend user interfaces with seamless integration between the two.

## 🏗️ Framework Architecture

### Structure
```
backendAutomationFramework/
├── config/
│   └── settings.py              # Centralized configuration
├── utils/
│   ├── http_client.py           # API client with auth support
│   ├── browser_client.py        # Playwright browser client
│   ├── auth_helper.py           # Authentication utilities
│   ├── data_parser.py           # Generic data file parser
│   └── logger.py                # Comprehensive logging
├── tests/
│   ├── api/                     # API-only tests
│   ├── ui/                      # UI-only tests
│   ├── hybrid/                  # Combined API+UI tests
│   └── test_apollo/             # Existing Apollo tests
├── data/
│   ├── api/                     # API test data
│   │   ├── requests/            # Request templates
│   │   ├── responses/           # Expected responses
│   │   └── schemas/             # JSON schemas
│   └── ui/                      # UI test data
│       ├── pages/               # Page object data
│       ├── elements/            # Element selectors
│       └── testdata/            # Test scenarios
├── reports/                     # Test reports
├── logs/                        # Execution logs
└── screenshots/                 # Failure screenshots
```

## 🚀 Quick Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
playwright install
```

2. **Configure settings** in `config/settings.py` or set environment variables.

3. **Run tests:**
```bash
# Run all tests
python run_tests.py

# Run specific test types
python run_tests.py --test-path tests/api/          # API tests only
python run_tests.py --test-path tests/ui/           # UI tests only
python run_tests.py --test-path tests/hybrid/       # Hybrid tests

# Run with different browsecoors
python run_tests.py --browser firefox --headed     # Firefox with GUI
python run_tests.py --browser webkit --headless    # Safari headless
```

## ⚙️ Configuration

The framework supports comprehensive configuration through environment variables:

```bash
# API Configuration
APOLLO_URL=https://apollo.welocalize.io
AUTH_TOKEN=your_auth_token_here

# UI Automation Configuration
BROWSER_TYPE=chromium          # chromium, firefox, webkit
HEADLESS_MODE=auto             # auto, true, false, debug
VIEWPORT_WIDTH=1920           # pixels
VIEWPORT_HEIGHT=1080          # pixels

# Timeout Configuration (milliseconds)
DEFAULT_TIMEOUT=30000          # Default element timeout
NAVIGATION_TIMEOUT=60000       # Page navigation timeout
ELEMENT_TIMEOUT=30000         # Element interaction timeout

# Screenshot & Video Configuration
SCREENSHOT_ON_FAILURE=true     # Take screenshot on test failure
VIDEO_RECORDING=false          # Enable video recording
SCREENSHOT_PATH=screenshots    # Directory for screenshots
VIDEO_PATH=videos              # Directory for videos

# Performance Monitoring
ENABLE_PERFORMANCE_MONITORING=false
ENABLE_NETWORK_MONITORING=false
```

## 🎯 Key Features

### ✅ **Hybrid Testing Capabilities**
- **API Testing**: Fast, reliable backend validation
- **UI Testing**: Comprehensive frontend automation  
- **Hybrid Scenarios**: End-to-end workflows combining API and UI
- **Shared Authentication**: Seamless token sharing between API and UI tests

### ✅ **Advanced Browser Automation**
- **Playwright Integration**: Modern, fast browser automation
- **Cross-Browser Support**: Chrome, Firefox, Safari
- **Mobile Device Emulation**: iPhone, Samsung Galaxy, iPad
- **Headless/Headed Modes**: Flexible execution options
- **Screenshot & Video Recording**: Automatic failure capture

### ✅ **Data Management**
- **Generic Data Parser**: Read/write JSON, YAML, CSV, TXT files
- **Variable Resolution**: Automatic environment variable substitution
- **File Caching**: Performance optimization for frequently accessed files
- **Organized Structure**: Separate data folders for API and UI

### ✅ **Reporting & Logging**
- **Multiple Report Formats**: HTML, Allure, Coverage reports
- **Comprehensive Logging**: Detailed execution logs with timestamps
- **Failure Analysis**: Screenshots, videos, and detailed error information
- **CI/CD Integration**: GitHub Actions workflows with artifact upload

## 💻 Usage Examples

### API Testing
```python
from utils.http_client import APIClient
from utils.auth_helper import AuthHelper
from config.settings import config

# Without authentication
client = APIClient(config.APOLLO_URL)
response = client.get("/health")

# With authentication
auth = AuthHelper("your_token")
client = APIClient(config.APOLLO_URL, auth)
response = client.get("/protected")
```

### UI Testing
```python
from utils.browser_client import browser_client
from config.settings import config

# Navigate and interact
await browser_client.navigate_to(config.APOLLO_URL)
await browser_client.click("#login-button")
await browser_client.fill("#username", "testuser")
await browser_client.take_screenshot("login_page")
```

### Data Management
```python
from utils.data_parser import data_parser

# Read test data
users = data_parser.read_json("ui", "testdata", "users.json")
api_config = data_parser.read_yaml("api", "config.yaml")

# Write results
data_parser.write_json(test_results, "reports", "results.json")
data_parser.write_csv(export_data, "exports", "data.csv")
```

### Hybrid Testing
```python
# API setup
auth = AuthHelper("token")
client = APIClient(config.APOLLO_URL, auth)
response = client.post("/setup", data=test_data)

# UI validation
await browser_client.navigate_to(config.DASHBOARD_URL)
assert "Success" in await browser_client.get_text(".status-message")

# API verification
verify_response = client.get("/verify")
assert verify_response.status_code == 200
```

## 🧪 Test Execution

### Command Line Options
```bash
# Basic test execution
python run_tests.py                                    # Run all tests
python run_tests.py --test-path tests/api/            # API tests only
python run_tests.py --test-path tests/ui/             # UI tests only
python run_tests.py --test-path tests/hybrid/         # Hybrid tests

# Reporting options
python run_tests.py --report html                     # HTML report
python generate_allure_html.py run                    # Allure report (run tests + generate)
python generate_allure_html.py                        # Generate Allure report from existing results
python generate_allure_html.py serve                  # Serve Allure report on local server

# Browser options
python run_tests.py --browser firefox                 # Use Firefox
python run_tests.py --browser webkit                  # Use Safari
python run_tests.py --headed                          # Run with GUI
python run_tests.py --headless                        # Run headless

# Test filtering
python run_tests.py --markers smoke                   # Run smoke tests
python run_tests.py --markers "not slow"              # Skip slow tests

# Setup and maintenance
python run_tests.py --setup                           # Setup framework
```

### Direct pytest Usage
```bash
# Run all tests
pytest tests/

# Run with HTML report
pytest tests/ --html=reports/report.html --self-contained-html

# Run with Allure (results are automatically generated)
pytest tests/ -v -s

# Generate Allure HTML report
python generate_allure_html.py

# Run tests and generate Allure report in one command
python generate_allure_html.py run

# Serve Allure report on local server
python generate_allure_html.py serve

# Run specific test types
pytest tests/api/ -v                                  # API tests
pytest tests/ui/ -v                                   # UI tests
pytest tests/hybrid/ -v                               # Hybrid tests
```

## 📊 Reports & Results

### Generated Reports
- **HTML Report**: `reports/report.html` - Detailed test results with screenshots
- **Coverage Report**: `reports/coverage/index.html` - Code coverage analysis
- **Allure Results**: `allure-results/` - Advanced reporting with trends
- **Log Files**: `logs/` - Detailed execution logs with timestamps
- **Screenshots**: `screenshots/` - Failure screenshots
- **Videos**: `videos/` - Test execution recordings

### 🎭 Allure Reporting

The framework automatically generates Allure results when running tests. Here are the different ways to work with Allure reports:

#### Method 1: Run Tests and Generate Report (Recommended)
```bash
# Run tests and generate Allure report in one command
python generate_allure_html.py run

# Run specific test path and generate report
python generate_allure_html.py run tests/api/
```

#### Method 2: Generate Report from Existing Results
```bash
# First run tests (Allure results are automatically generated)
pytest tests/ -v -s

# Then generate HTML report
python generate_allure_html.py
```

#### Method 3: Serve Report on Local Server (Best for Viewing)
```bash
# Serve Allure report on local server (opens in browser automatically)
python generate_allure_html.py serve
```

#### Method 4: Direct pytest Commands
```bash
# Run tests with Allure results (already configured in pytest.ini)
pytest tests/ -v -s

# Run specific test file
pytest tests/api/test_apollo/test_apollo.py -v -s

# Run with additional Allure options
pytest tests/ -v -s --alluredir=allure-results --clean-alluredir
```

### Viewing Reports
```bash
# View HTML report
start reports/report.html

# View coverage report
start reports/coverage/index.html

# Generate and view Allure report
python generate_allure_html.py

# Alternative: Run tests and generate report in one command
python generate_allure_html.py run

# Serve Allure report on local server (recommended for viewing)
python generate_allure_html.py serve
```

## 🚀 CI/CD Integration

### GitHub Actions
The framework includes comprehensive CI/CD workflows:
- **Multi-Python Testing**: Python 3.9, 3.10, 3.11
- **Automated Reports**: HTML, Allure, Coverage
- **Artifact Upload**: Test results and reports
- **PR Integration**: Automatic test results in pull requests

### Quick CI Setup
1. Push code to GitHub repository
2. Enable GitHub Actions in repository settings
3. Set environment variables (optional)
4. Tests run automatically on push/PR

### Environment Variables for CI/CD
```bash
# API URLs (if different from defaults)
APOLLO_URL=https://apollo.welocalize.io
AIQE_URL=https://your-aiqe-api.com
APIE_URL=https://your-apie-api.com

# Authentication (if needed)
AUTH_TOKEN=your-auth-token

# Test Configuration
TEST_TIMEOUT=60
LOG_LEVEL=INFO
RETRY_COUNT=3

# Reporting
GENERATE_ALLURE=true
GENERATE_COVERAGE=true
GENERATE_HTML=true
UPLOAD_ARTIFACTS=true

# Parallel Execution
PARALLEL_WORKERS=2
```

## 🧹 Maintenance

### Cleanup
```bash
# Preview cleanup
python cleanup.py --preview

# Clean all generated files
python cleanup.py
```

### Framework Setup
```bash
# Complete setup
python run_tests.py --setup
```

## 🎯 Test Types

1. **API Tests**: Fast, reliable backend testing
2. **UI Tests**: User interface validation with Playwright
3. **Hybrid Tests**: End-to-end scenarios combining API and UI

## 🔧 Advanced Configuration

### Browser Configuration
```bash
# Browser Settings
BROWSER_TYPE=chromium          # chromium, firefox, webkit
HEADLESS=true                  # true, false (legacy)
VIEWPORT_WIDTH=1920           # pixels
VIEWPORT_HEIGHT=1080          # pixels

# Enhanced Headless Mode Control
HEADLESS_MODE=auto             # auto, true, false, debug
HEADLESS_DEBUG=false           # Show browser in debug mode
HEADLESS_SLOW_MO=0             # Slow down operations (ms)
```

### Screenshot & Video Configuration
```bash
# Screenshot Settings
SCREENSHOT_ON_FAILURE=true     # Take screenshot on test failure
SCREENSHOT_ON_SUCCESS=false    # Take screenshot on test success
SCREENSHOT_FULL_PAGE=true      # Capture full page or viewport only
SCREENSHOT_PATH=screenshots    # Directory for screenshots
SCREENSHOT_FORMAT=png          # png, jpeg
SCREENSHOT_QUALITY=90          # Quality for JPEG (1-100)

# Video Recording Settings
VIDEO_RECORDING=false          # Enable video recording
VIDEO_ON_FAILURE=true          # Record video on test failure
VIDEO_ON_SUCCESS=false         # Record video on test success
VIDEO_PATH=videos              # Directory for videos
VIDEO_FORMAT=webm              # webm, mp4
VIDEO_QUALITY=medium           # low, medium, high
```

### Performance & Network Monitoring
```bash
# Performance Monitoring
ENABLE_PERFORMANCE_MONITORING=false
PERFORMANCE_THRESHOLD=5000     # Performance threshold (ms)
TRACK_METRICS=load_time,dom_content_loaded,first_paint

# Network Monitoring
ENABLE_NETWORK_MONITORING=false
LOG_NETWORK_REQUESTS=false
BLOCK_NETWORK_REQUESTS=false
```

### Mobile Device Emulation
```bash
# Mobile Device Settings
MOBILE_DEVICE=none             # none, iPhone_12, Samsung_Galaxy_S21, iPad
```

**Pre-configured Devices:**
- **iPhone_12**: 390x844, iOS Safari
- **Samsung_Galaxy_S21**: 384x854, Android Chrome
- **iPad**: 768x1024, iOS Safari

## 🎭 Cursor IDE Setup

### Install Required Extensions
1. **Python** by Microsoft
2. **Playwright Test for VSCode** by Microsoft
3. **Pytest** by Little Fox Team (optional but helpful)

### Configure .vscode/settings.json
```json
{
    "python.defaultInterpreterPath": "python",
    "python.terminal.activateEnvironment": true,
    "playwright.reuseBrowser": true,
    "playwright.showTrace": true,
    "playwright.baseURL": "https://apollo.welocalize.io",
    "playwright.testDir": "tests",
    "playwright.outputDir": "test-results",
    "playwright.reporters": ["html", "allure"],
    "playwright.timeout": 30000,
    "playwright.retries": 3,
    "playwright.workers": 1,
    "playwright.headed": false,
    "playwright.debug": false,
    "playwright.trace": "on-first-retry",
    "playwright.video": "retain-on-failure",
    "playwright.screenshot": "only-on-failure",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests"],
    "python.testing.unittestEnabled": false,
    "python.testing.autoTestDiscoverOnSaveEnabled": true
}
```

### Environment Variables for Development
```bash
# Simple Headless Control
RUN_HEADLESS=false

# Browser Configuration
BROWSER_TYPE=chromium
VIEWPORT_WIDTH=1920
VIEWPORT_HEIGHT=1080

# Screenshot Configuration
SCREENSHOT_ON_FAILURE=true
SCREENSHOT_FAILED_TESTS_ONLY=true
SCREENSHOT_PATH=screenshots

# Video Recording Configuration
VIDEO_RECORDING=true
VIDEO_FAILED_TESTS_ONLY=true
VIDEO_PATH=videos

# Debug Configuration
HEADLESS_DEBUG=true
HEADLESS_SLOW_MO=1000

# API Configuration
APOLLO_URL=https://apollo.welocalize.io
AUTH_TOKEN=your_token_here

# Logging
LOG_LEVEL=DEBUG
```

## 🆘 Troubleshooting

### Common Issues

#### **Browser Not Opening**
```bash
# Check if RUN_HEADLESS is set correctly
echo $RUN_HEADLESS

# Try running with explicit headless=false
RUN_HEADLESS=false python run_ui_tests.py
```

#### **Playwright Not Found**
```bash
# Reinstall Playwright
pip uninstall playwright
pip install playwright
playwright install
```

#### **Tests Not Running**
```bash
# Check Python path
which python

# Check pytest installation
pytest --version

# Run with verbose output
pytest -v -s
```

#### **Import Errors**
```bash
# Check if all dependencies are installed
pip install -r requirements.txt

# Check Python path in settings
# Make sure python.defaultInterpreterPath is correct
```

### Pytest Discovery Issues
If Cursor shows "pytest Discovery Error":

1. **Check Python Interpreter**:
   - Press `Ctrl+Shift+P`
   - Type "Python: Select Interpreter"
   - Select the correct Python interpreter

2. **Update .vscode/settings.json** with proper Python configuration

3. **Create pytest.ini**:
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    -s
    --tb=short
    --html=reports/report.html
    --self-contained-html
    --alluredir=allure-results
    --cov=utils
    --cov=config
    --cov-report=html:htmlcov
    --cov-report=term-missing
markers =
    ui: UI tests
    api: API tests
    hybrid: Hybrid tests
    slow: Slow tests
    smoke: Smoke tests
asyncio_mode = auto
```

4. **Restart Cursor** completely after configuration

## 📈 Performance & Best Practices

### Development Environment
```bash
HEADLESS_MODE=false
SCREENSHOT_ON_FAILURE=true
SCREENSHOT_FAILED_TESTS_ONLY=false
VIDEO_RECORDING=false
LOG_LEVEL=DEBUG
ENABLE_NETWORK_MONITORING=true
```

### CI/CD Environment
```bash
HEADLESS_MODE=auto
SCREENSHOT_ON_FAILURE=true
SCREENSHOT_FAILED_TESTS_ONLY=true
VIDEO_RECORDING=true
VIDEO_FAILED_TESTS_ONLY=true
LOG_LEVEL=INFO
ENABLE_NETWORK_MONITORING=false
```

### Debug Environment
```bash
HEADLESS_MODE=debug
HEADLESS_DEBUG=true
HEADLESS_SLOW_MO=1000
SCREENSHOT_ON_FAILURE=true
VIDEO_RECORDING=true
LOG_LEVEL=DEBUG
```

## 🎯 Framework Benefits

### **Choose This Framework When:**
- ✅ You need **unified API + UI testing**
- ✅ You require **advanced reporting and analytics**
- ✅ You have **complex data management needs**
- ✅ You need **comprehensive CI/CD integration**
- ✅ You want **enterprise-grade testing capabilities**
- ✅ You have **Python expertise in your team**

### **Key Advantages:**
1. **Unified Testing**: Seamless API + UI testing in one framework
2. **Advanced Features**: Comprehensive reporting, data management, and CI/CD
3. **Enterprise Readiness**: Production-ready with extensive configuration options
4. **Scalability**: Handles complex testing scenarios and large test suites
5. **Maintainability**: Well-structured, documented, and maintainable codebase

This framework provides a comprehensive solution for modern test automation with seamless integration between API and UI testing capabilities.