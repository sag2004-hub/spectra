import os
import re

def sanitize_filename(name):
    """Sanitize a string to be used as a filename"""
    # Remove invalid characters
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    # Replace spaces with underscores
    name = name.replace(' ', '_')
    # Limit length
    if len(name) > 50:
        name = name[:50]
    return name

def ensure_directory_exists(path):
    """Ensure a directory exists, create if it doesn't"""
    os.makedirs(path, exist_ok=True)
    return path