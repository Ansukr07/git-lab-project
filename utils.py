"""
Utility functions for file operations and logging.
"""
import os
import logging
import sys

def setup_logger(name=__name__):
    """
    Sets up a logger with standard formatting.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(name)

def safe_mkdir(path):
    """
    Creates a directory if it doesn't exist, safely.
    """
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            return True
        except OSError as e:
            print(f"Error creating directory {path}: {e}")
            return False
    return True

def validate_file(path):
    """
    Checks if a file exists.
    """
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return False
    return True

def get_files_by_extension(directory, extension):
    """
    Returns a list of files in a directory with a specific extension.
    """
    if not os.path.exists(directory):
        return []
    
    return [
        os.path.join(directory, f) 
        for f in os.listdir(directory) 
        if f.endswith(extension)
    ]
