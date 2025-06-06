#!/usr/bin/env python3
"""
E-Commerce Data Scraper - Professional Desktop Application
Main entry point for the application.

This application provides a professional interface for scraping product data
from legal e-commerce websites with proper rate limiting and data export capabilities.

Author: Portfolio Project
Version: 1.0.0
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox
import logging

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils.logger import setup_logging, get_logger
from utils.config import Config
from gui.main_window import MainWindow


def main():
    """Main entry point for the E-Commerce Data Scraper application."""
    try:
        # Setup logging
        setup_logging()
        logger = get_logger(__name__)
        logger.info("Starting E-Commerce Data Scraper Application")
        
        # Load configuration
        config = Config()
        logger.info("Configuration loaded successfully")
        
        # Create the main application window
        root = tk.Tk()
        app = MainWindow(root, config)
        
        # Start the application
        logger.info("Application GUI initialized, starting main loop")
        root.mainloop()
        
    except Exception as e:
        error_msg = f"Failed to start application: {str(e)}"
        print(error_msg)
        
        # Try to show error dialog if tkinter is available
        try:
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            messagebox.showerror("Application Error", error_msg)
        except:
            pass
        
        sys.exit(1)


if __name__ == "__main__":
    main()
