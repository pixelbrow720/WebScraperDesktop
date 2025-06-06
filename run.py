#!/usr/bin/env python3
"""
Convenient runner script for the E-Commerce Data Scraper application.
This script ensures proper environment setup before launching the main application.
"""

import sys
import os
import subprocess

def check_requirements():
    """Check if all required packages are installed."""
    try:
        import tkinter
        import requests
        import bs4
        import pandas
        import matplotlib
        import yaml
        import openpyxl
        return True
    except ImportError as e:
        print(f"Missing required package: {e}")
        print("Please install requirements using: pip install -r requirements.txt")
        return False

def main():
    """Main runner function."""
    print("E-Commerce Data Scraper - Professional Desktop Application")
    print("=" * 60)
    
    # Check if requirements are satisfied
    if not check_requirements():
        sys.exit(1)
    
    # Launch the main application
    try:
        from main import main as app_main
        app_main()
    except KeyboardInterrupt:
        print("\nApplication terminated by user.")
    except Exception as e:
        print(f"Error running application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
