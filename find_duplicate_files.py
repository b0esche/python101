#!/usr/bin/env python3
"""
Find Duplicate File Names Script

This script scans a directory and its subdirectories to find files with duplicate names.
It recursively traverses all subdirectories and groups files by their filename.
"""

import os
import sys
from collections import defaultdict

def find_duplicate_names(directory):
    """
    Find files with duplicate names in the given directory and subdirectories.

    Args:
        directory (str): Path to the directory to scan

    Returns:
        dict: Dictionary with filenames as keys and lists of full paths as values
    """
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory")
        return {}

    # Dictionary to store files grouped by name
    name_groups = defaultdict(list)

    # Traverse directory recursively
    for root, dirs, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            name_groups[filename].append(filepath)

    # Collect only groups with duplicates (more than one file with same name)
    duplicates = {name: paths for name, paths in name_groups.items() if len(paths) > 1}

    return duplicates

def print_duplicates(duplicates):
    """
    Print the found duplicate filenames in a readable format.
    """
    if not duplicates:
        print("No duplicate filenames found.")
        return

    print(f"Found {len(duplicates)} filenames that appear multiple times:")
    print("=" * 60)

    for filename, filepaths in duplicates.items():
        print(f"Filename: '{filename}' (appears {len(filepaths)} times)")
        for filepath in filepaths:
            try:
                file_size = os.path.getsize(filepath)
                print(f"  {filepath} ({file_size} bytes)")
            except OSError:
                print(f"  {filepath} (size unknown)")
        print()

def main():
    """
    Main function to run the duplicate filename finder.
    """
    if len(sys.argv) != 2:
        print("Usage: python find_duplicate_files.py <directory>")
        print("Example: python find_duplicate_files.py /path/to/directory")
        sys.exit(1)

    directory = sys.argv[1]
    print(f"Scanning directory: {directory}")
    print("Looking for duplicate filenames...")

    duplicates = find_duplicate_names(directory)
    print_duplicates(duplicates)

if __name__ == "__main__":
    main()