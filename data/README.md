# Test Data Organization

This directory contains all test data organized by type and purpose. The data parser provides generic methods to read/write any file type.

## Directory Structure

```
data/
├── api/
│   ├── requests/          # API request templates
│   ├── responses/         # Expected API responses
│   └── schemas/          # JSON schemas for validation
├── ui/
│   ├── pages/            # Page object data
│   ├── elements/         # Common element selectors
│   └── testdata/         # Test data (users, scenarios, etc.)
└── fixtures/             # General test fixtures
```

## Generic File Operations

### Text Files
```python
from utils.data_parser import data_parser

# Read any text file
content = data_parser.read_file("api", "requests", "my_requests.txt")

# Write text file
data_parser.write_file("Hello World", "output", "result.txt")

# Append to file
data_parser.append_file("New line\n", "logs", "test.log")
```

### JSON Files
```python
# Read JSON file
data = data_parser.read_json("api", "requests", "apollo_requests.json")

# Write JSON file
request_data = {"method": "GET", "endpoint": "/health"}
data_parser.write_json(request_data, "api", "requests", "new_request.json")

# Get specific value from JSON
username = data_parser.get_json_value("ui", "testdata", "users.json", key="user.profile.username")
```

### YAML Files
```python
# Read YAML file
config = data_parser.read_yaml("config", "test_config.yaml")

# Write YAML file
data_parser.write_yaml({"browser": "chrome", "headless": True}, "config", "browser.yaml")
```

### CSV Files
```python
# Read CSV as list of dictionaries
users = data_parser.read_csv("ui", "testdata", "users.csv")

# Read CSV as list of lists
raw_data = data_parser.read_csv("ui", "testdata", "users.csv", as_dict=False)

# Write CSV file
user_data = [{"name": "John", "email": "john@example.com"}]
data_parser.write_csv(user_data, "output", "exported_users.csv")
```

## Utility Methods

```python
# Check if file exists
exists = data_parser.file_exists("api", "requests", "my_file.json")

# Create directory
data_parser.create_directory("new", "subdirectory")

# List files in directory
files = data_parser.list_files("api", "requests", pattern="*.json")

# Clear cache
data_parser.clear_cache()

# Get cache info
cache_info = data_parser.get_cache_info()
```

## Variable Resolution

The data parser automatically resolves environment variables in the format `${VARIABLE_NAME}`:

```json
{
  "username": "${TEST_USERNAME}",
  "password": "${TEST_PASSWORD}",
  "base_url": "${APOLLO_URL}"
}
```

These will be replaced with values from `config.settings`.

## File Path Examples

```python
# All these are equivalent ways to specify file paths:
data_parser.read_json("api", "requests", "apollo.json")
data_parser.read_json("api/requests/apollo.json")
data_parser.read_json("api", "requests", "apollo.json")

# Results in: data/api/requests/apollo.json
```

## Best Practices

1. Use descriptive names for data files
2. Keep related data together in the same file
3. Use environment variables for sensitive data
4. Validate file syntax before committing
5. Use appropriate file types (JSON for structured data, TXT for simple text, CSV for tabular data)
6. Leverage caching for frequently accessed files
