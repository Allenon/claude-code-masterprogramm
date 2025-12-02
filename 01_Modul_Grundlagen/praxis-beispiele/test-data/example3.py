# example3.py - File operations
import os
import json

def read_json_file(filepath: str) -> dict:
    """Read JSON file"""
    with open(filepath, 'r') as f:
        return json.load(f)

# TODO: Add write_json_file function
# TODO: Add error handling
