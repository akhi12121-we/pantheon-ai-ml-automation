# Cursor IDE Quick Reference - Backend Automation Framework

## 🚀 Quick Setup (5 Minutes)

### 1. Clone & Setup
```bash
git clone <repository-url>
cd backendAutomationFramework
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Cursor IDE Setup
1. Open project in Cursor IDE
2. Install extensions: **Python**, **Pytest**, **Allure**
3. `Ctrl+Shift+P` → "Python: Select Interpreter" → Select `.venv\Scripts\python.exe`
4. `Ctrl+Shift+P` → "Preferences: Open Workspace Settings (JSON)" → Add configuration

### 3. Verify Setup
```bash
pytest tests/api/test_apollo/test_apollo.py::TestApollo::test_health_check -v -s
```

---

## 🧪 Running Tests

### In Cursor IDE
- **Test Explorer**: `Ctrl+Shift+T` → Click Run
- **Command Palette**: `Ctrl+Shift+P` → "Python: Run All Tests"
- **Terminal**: `pytest tests/ -v -s`

### Framework Commands
```bash
# Run tests with Allure report
python generate_allure_html.py run

# Run specific test path
python generate_allure_html.py run tests/ui/test_simple_ui.py

# Clean and run
python generate_allure_html.py clean
pytest tests/ -v -s
```

---

## 📊 Allure Reports

### Generate & View
```bash
# Recommended: Run tests and serve report
python generate_allure_html.py run tests/ui/test_simple_ui.py

# Alternative: Generate and serve existing results
python generate_allure_html.py generate-serve

# Serve existing report
python generate_allure_html.py serve
```

### Important Notes
- ✅ Always use `serve` command (no 404 errors)
- ✅ Report opens automatically in browser
- ✅ Use `Ctrl+C` to stop server when done

---

## 🔧 Configuration Files

### Essential Files
- `pytest.ini` - Test configuration
- `.vscode/settings.json` - Cursor IDE settings
- `config/settings.py` - Framework configuration
- `.env` - Environment variables

### Key Settings
```json
{
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["-s", "--capture=no"],
    "python.testing.showOutput": true,
    "terminal.integrated.env.windows": {
        "PYTHONPATH": "${workspaceFolder}"
    }
}
```

---

## 🐛 Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| Tests not discovered | Reload window (`Ctrl+Shift+P` → "Developer: Reload Window") |
| Import errors | Check Python interpreter and PYTHONPATH |
| Print not visible | Use `logger.info()` or `ide_output.force_print()` |
| Allure 404 errors | Use `python generate_allure_html.py serve` |
| Browser tests fail | Run `playwright install` |

---

## 📁 Project Structure

```
backendAutomationFramework/
├── tests/
│   ├── api/test_apollo/     # API tests
│   └── ui/                  # UI tests
├── utils/                   # Framework utilities
├── config/                  # Configuration files
├── allure-results/          # Allure test results
├── allure-report/           # Generated reports
├── logs/                    # Test execution logs
├── screenshots/             # Failure screenshots
└── videos/                  # Test recordings
```

---

## 🎯 Test Types

### API Tests
```bash
pytest tests/api/ -v -s
python generate_allure_html.py run tests/api/test_apollo/
```

### UI Tests
```bash
pytest tests/ui/ -v -s
python generate_allure_html.py run tests/ui/test_simple_ui.py
```

### With Markers
```bash
pytest -m smoke -v -s        # Smoke tests only
pytest -m "not slow" -v -s   # Skip slow tests
pytest -m api -v -s          # API tests only
```

---

## 📝 Best Practices

### ✅ Do
- Use virtual environment
- Run tests with `-v -s` flags
- Use serve command for Allure reports
- Check logs in `logs/` directory
- Use descriptive test names

### ❌ Don't
- Open Allure HTML files directly
- Run tests without virtual environment
- Ignore import errors
- Skip configuration steps

---

## 🆘 Emergency Commands

### Reset Everything
```bash
# Clean all results
python generate_allure_html.py clean

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Reinstall Playwright
playwright install --force
```

### Debug Mode
```bash
# Run with maximum verbosity
pytest tests/ -vvv -s --tb=long

# Run single test with debug
pytest tests/api/test_apollo/test_apollo.py::TestApollo::test_health_check -vvv -s --tb=long
```

---

## 📞 Support

- **Full Guide**: See `CURSOR_IDE_SETUP_GUIDE.md`
- **Project README**: See `README.md`
- **Logs**: Check `logs/` directory
- **Issues**: Contact automation team

---

*Last updated: September 2025*
