#!/usr/bin/env python3
"""
Simple Config Parser Utility for reading configuration files.
"""
import configparser
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from config.settings import config

def get_config_value(section: str, key: str, file_path):
    """Read config file and return value based on section.key."""
    file_path = os.path.join(config.UI_TESTDATA_PATH, file_path)
    config_parser = configparser.ConfigParser()
    config_parser.read(file_path)
    return config_parser.get(section, key)
