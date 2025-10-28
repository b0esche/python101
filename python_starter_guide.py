#!/usr/bin/env python3
"""
Python Starter Guide: Essential Imports and Structure for New Scripts

This script demonstrates the most commonly used imports and basic structure
to help you start creating your own Python scripts. Each section includes
helpful comments explaining why and how to use these elements.
"""

# Essential imports for file system operations
import os  # Provides functions for interacting with the operating system
import sys  # Gives access to system-specific parameters and functions

# Imports for working with dates and times
import datetime  # For date and time manipulation
from datetime import timedelta  # For time intervals

# Imports for data handling
import json  # For JSON data serialization/deserialization
import csv  # For reading/writing CSV files

# Imports for random number generation and math
import random  # For generating random numbers
import math  # For mathematical functions

# Imports for command-line argument parsing (useful for scripts)
import argparse  # For parsing command-line arguments

# Optional: For HTTP requests (uncomment if needed)
# import requests  # For making HTTP requests to APIs

# Optional: For logging (uncomment if needed)
# import logging  # For logging messages and errors

def get_system_info():
    """
    Function demonstrating basic system information retrieval.
    This shows how to use os and sys modules.
    """
    print("=== System Information ===")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python version: {sys.version}")
    print(f"Platform: {sys.platform}")
    print(f"Script name: {sys.argv[0]}")
    return True

def work_with_dates():
    """
    Function demonstrating date and time operations.
    Shows how to use datetime module for common date tasks.
    """
    print("\n=== Date and Time Operations ===")
    now = datetime.datetime.now()
    print(f"Current date and time: {now}")
    print(f"Current date: {now.date()}")
    print(f"Current time: {now.time()}")

    # Formatting dates
    print(f"Formatted date: {now.strftime('%Y-%m-%d %H:%M:%S')}")

    # Date arithmetic
    tomorrow = now + timedelta(days=1)
    print(f"Tomorrow: {tomorrow.date()}")

    return now

def handle_data_structures():
    """
    Function demonstrating data handling with JSON and CSV.
    Shows how to read/write structured data.
    """
    print("\n=== Data Handling ===")

    # Working with JSON
    sample_data = {
        "name": "Python Script",
        "version": "1.0",
        "features": ["imports", "functions", "comments"]
    }

    # Convert to JSON string
    json_string = json.dumps(sample_data, indent=2)
    print("JSON data:")
    print(json_string)

    # Parse JSON back to Python object
    parsed_data = json.loads(json_string)
    print(f"Parsed name: {parsed_data['name']}")

    # Working with CSV (in-memory example)
    csv_data = [
        ["Name", "Age", "City"],
        ["Alice", "25", "New York"],
        ["Bob", "30", "San Francisco"]
    ]

    print("\nCSV data:")
    for row in csv_data:
        print(", ".join(row))

    return sample_data

def demonstrate_math_and_random():
    """
    Function demonstrating mathematical operations and random number generation.
    Shows basic math functions and random utilities.
    """
    print("\n=== Math and Random Operations ===")

    # Math operations
    numbers = [1, 2, 3, 4, 5]
    print(f"Sum: {sum(numbers)}")
    print(f"Average: {sum(numbers) / len(numbers)}")
    print(f"Square root of 16: {math.sqrt(16)}")
    print(f"Pi: {math.pi}")

    # Random operations
    print(f"Random number (0-1): {random.random()}")
    print(f"Random integer (1-10): {random.randint(1, 10)}")
    print(f"Random choice from list: {random.choice(['apple', 'banana', 'cherry'])}")

    return numbers

def parse_arguments():
    """
    Function demonstrating command-line argument parsing.
    Shows how to make scripts configurable via command line.
    """
    print("\n=== Command Line Arguments ===")

    parser = argparse.ArgumentParser(description="Python Starter Guide Script")
    parser.add_argument("--name", default="World", help="Name to greet")
    parser.add_argument("--count", type=int, default=1, help="Number of greetings")

    # Note: In a real script, you'd use parser.parse_args()
    # Here we simulate with default values
    args = parser.parse_args([])  # Empty list for demonstration

    print(f"Parsed arguments: name='{args.name}', count={args.count}")

    for i in range(args.count):
        print(f"Hello, {args.name}!")

    return args

def main():
    """
    Main function that orchestrates the script execution.
    This is the entry point of the script.
    """
    print("Welcome to the Python Starter Guide!")
    print("=" * 50)

    try:
        # Execute each demonstration function
        get_system_info()
        work_with_dates()
        handle_data_structures()
        demonstrate_math_and_random()
        parse_arguments()

        print("\n=== Script completed successfully! ===")
        print("You can now use these imports and patterns in your own scripts.")
        print("Remember to:")
        print("- Add docstrings to your functions")
        print("- Use meaningful variable names")
        print("- Handle errors with try/except blocks")
        print("- Test your code thoroughly")

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

# This ensures the script runs only when executed directly, not when imported
if __name__ == "__main__":
    main()