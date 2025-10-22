#!/usr/bin/env python3
"""
Generic data parser utility for reading and writing various file types.
"""
import json
import os
import csv
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from config.settings import config
from utils.logger import logger

# Optional yaml import - only import if available
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

class DataParser:
    """Generic utility class for reading and writing various file types."""
    
    def __init__(self, data_root: str = "data"):
        self.data_root = Path(data_root)
        self.cache = {}  # Cache for loaded files
    
    def _get_file_path(self, *path_parts: str) -> Path:
        """Build file path from parts."""
        return self.data_root / Path(*path_parts)
    
    def _resolve_variables(self, data: Any) -> Any:
        """Resolve environment variables in data."""
        if isinstance(data, dict):
            return {key: self._resolve_variables(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self._resolve_variables(item) for item in data]
        elif isinstance(data, str) and data.startswith("${") and data.endswith("}"):
            # Extract variable name and resolve from config
            var_name = data[2:-1]
            return getattr(config, var_name, data)
        else:
            return data
    
    # Generic File Operations
    def read_file(self, *path_parts: str, encoding: str = 'utf-8') -> str:
        """Read any text file."""
        file_path = self._get_file_path(*path_parts)
        
        if str(file_path) in self.cache:
            return self.cache[str(file_path)]
        
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
                self.cache[str(file_path)] = content
                logger.debug(f"Read file: {file_path}")
                return content
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            return ""
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return ""
    
    def write_file(self, content: str, *path_parts: str, encoding: str = 'utf-8') -> bool:
        """Write content to any text file."""
        file_path = self._get_file_path(*path_parts)
        
        try:
            # Create directory if it doesn't exist
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(content)
            
            # Update cache
            self.cache[str(file_path)] = content
            logger.info(f"Written file: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error writing file {file_path}: {e}")
            return False
    
    def append_file(self, content: str, *path_parts: str, encoding: str = 'utf-8') -> bool:
        """Append content to any text file."""
        file_path = self._get_file_path(*path_parts)
        
        try:
            # Create directory if it doesn't exist
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'a', encoding=encoding) as f:
                f.write(content)
            
            logger.info(f"Appended to file: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error appending to file {file_path}: {e}")
            return False
    
    # JSON Operations
    def read_json(self, *path_parts: str, resolve_vars: bool = True) -> Union[Dict, List, None]:
        """Read JSON file."""
        file_path = self._get_file_path(*path_parts)
        
        if str(file_path) in self.cache:
            data = self.cache[str(file_path)]
            return self._resolve_variables(data) if resolve_vars else data
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.cache[str(file_path)] = data
                logger.debug(f"Read JSON file: {file_path}")
                return self._resolve_variables(data) if resolve_vars else data
        except FileNotFoundError:
            logger.error(f"JSON file not found: {file_path}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in file {file_path}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error reading JSON file {file_path}: {e}")
            return None
    
    def write_json(self, data: Union[Dict, List], *path_parts: str, indent: int = 2) -> bool:
        """Write data to JSON file."""
        file_path = self._get_file_path(*path_parts)
        
        try:
            # Create directory if it doesn't exist
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent, ensure_ascii=False)
            
            # Update cache
            self.cache[str(file_path)] = data
            logger.info(f"Written JSON file: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error writing JSON file {file_path}: {e}")
            return False
    
    def get_json_value(self, *path_parts: str, key: str = None, resolve_vars: bool = True) -> Any:
        """Get specific value from JSON file."""
        data = self.read_json(*path_parts, resolve_vars=resolve_vars)
        if data is None:
            return None
        
        if key is None:
            return data
        
        # Support nested keys like "user.profile.name"
        keys = key.split('.')
        for k in keys:
            if isinstance(data, dict) and k in data:
                data = data[k]
            else:
                return None
        return data
    
    # YAML Operations
    def read_yaml(self, *path_parts: str, resolve_vars: bool = True) -> Union[Dict, List, None]:
        """Read YAML file."""
        if not YAML_AVAILABLE:
            logger.error("YAML module not available. Install PyYAML to use YAML functionality.")
            return None
            
        file_path = self._get_file_path(*path_parts)
        
        if str(file_path) in self.cache:
            data = self.cache[str(file_path)]
            return self._resolve_variables(data) if resolve_vars else data
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                self.cache[str(file_path)] = data
                logger.debug(f"Read YAML file: {file_path}")
                return self._resolve_variables(data) if resolve_vars else data
        except FileNotFoundError:
            logger.error(f"YAML file not found: {file_path}")
            return None
        except yaml.YAMLError as e:
            logger.error(f"Invalid YAML in file {file_path}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error reading YAML file {file_path}: {e}")
            return None
    
    def write_yaml(self, data: Union[Dict, List], *path_parts: str) -> bool:
        """Write data to YAML file."""
        if not YAML_AVAILABLE:
            logger.error("YAML module not available. Install PyYAML to use YAML functionality.")
            return False
            
        file_path = self._get_file_path(*path_parts)
        
        try:
            # Create directory if it doesn't exist
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            
            # Update cache
            self.cache[str(file_path)] = data
            logger.info(f"Written YAML file: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error writing YAML file {file_path}: {e}")
            return False
    
    # CSV Operations
    def read_csv(self, *path_parts: str, as_dict: bool = True) -> Union[List[Dict], List[List], None]:
        """Read CSV file."""
        file_path = self._get_file_path(*path_parts)
        
        try:
            with open(file_path, 'r', encoding='utf-8', newline='') as f:
                if as_dict:
                    reader = csv.DictReader(f)
                    data = list(reader)
                else:
                    reader = csv.reader(f)
                    data = list(reader)
                logger.debug(f"Read CSV file: {file_path}")
                return data
        except FileNotFoundError:
            logger.error(f"CSV file not found: {file_path}")
            return None
        except Exception as e:
            logger.error(f"Error reading CSV file {file_path}: {e}")
            return None
    
    def write_csv(self, data: List[Dict], *path_parts: str, fieldnames: List[str] = None) -> bool:
        """Write data to CSV file."""
        file_path = self._get_file_path(*path_parts)
        
        try:
            # Create directory if it doesn't exist
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            if not data:
                return False
            
            # Get fieldnames from first row if not provided
            if fieldnames is None:
                fieldnames = list(data[0].keys())
            
            with open(file_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            
            logger.info(f"Written CSV file: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error writing CSV file {file_path}: {e}")
            return False
    
    # Utility Methods
    def file_exists(self, *path_parts: str) -> bool:
        """Check if file exists."""
        file_path = self._get_file_path(*path_parts)
        return file_path.exists()
    
    def create_directory(self, *path_parts: str) -> bool:
        """Create directory."""
        dir_path = self._get_file_path(*path_parts)
        try:
            dir_path.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Created directory: {dir_path}")
            return True
        except Exception as e:
            logger.error(f"Error creating directory {dir_path}: {e}")
            return False
    
    def list_files(self, *path_parts: str, pattern: str = "*") -> List[str]:
        """List files in directory."""
        dir_path = self._get_file_path(*path_parts)
        if not dir_path.exists():
            return []
        
        try:
            files = [f.name for f in dir_path.glob(pattern)]
            return files
        except Exception as e:
            logger.error(f"Error listing files in {dir_path}: {e}")
            return []
    
    def clear_cache(self):
        """Clear the file cache."""
        self.cache.clear()
        logger.debug("Data parser cache cleared")
    
    def get_cache_info(self) -> Dict[str, str]:
        """Get cache information."""
        return {str(path): type(data).__name__ for path, data in self.cache.items()}
    
    def read_project_name(self) -> str:
        """Read project name from projectname.txt file."""
        try:
            project_name = self.read_file("projectname.txt")
            if project_name:
                logger.info(f"Read project name from file: {project_name.strip()}")
                return project_name.strip()
            else:
                logger.error("Project name file is empty")
                return ""
        except Exception as e:
            logger.error(f"Failed to read project name from file: {e}")
            return ""
    
    def get_opal_token(self) -> str:
        """Read auth token from Opal token generation response."""
        try:
            response_data = self.read_json("api", "response", "opaltokenGeneration.json")
            if response_data and "auth_token" in response_data:
                token = response_data["auth_token"]
                logger.info("Successfully retrieved Opal auth token")
                return token
            else:
                logger.error("Auth token not found in Opal response file")
                return ""
        except Exception as e:
            logger.error(f"Failed to read Opal auth token: {e}")
            return ""
    
    def get_opal_refresh_token(self) -> str:
        """Read refresh token from Opal token generation response."""
        try:
            response_data = self.read_json("api", "response", "opaltokenGeneration.json")
            if response_data and "refresh_token" in response_data:
                refresh_token = response_data["refresh_token"]
                logger.info("Successfully retrieved Opal refresh token")
                return refresh_token
            else:
                logger.error("Refresh token not found in Opal response file")
                return ""
        except Exception as e:
            logger.error(f"Failed to read Opal refresh token: {e}")
            return ""

# Global data parser instance
data_parser = DataParser()
