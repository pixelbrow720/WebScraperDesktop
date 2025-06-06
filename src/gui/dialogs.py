"""
Dialog windows for the E-Commerce Data Scraper application.
Contains progress dialogs, settings dialogs, and other modal windows.
"""

import tkinter as tk
from tkinter import ttk, messagebox


class ProgressDialog:
    """Progress dialog for long-running operations."""
    
    def __init__(self, parent, title="Progress", message="Please wait..."):
        self.parent = parent
        self.cancelled = False
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x150")
        self.dialog.resizable(False, False)
        
        # Center the dialog
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Create widgets
        self.setup_widgets(message)
        
        # Configure closing behavior
        self.dialog.protocol("WM_DELETE_WINDOW", self.on_cancel)
        
    def setup_widgets(self, message):
        """Setup dialog widgets."""
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Message label
        self.message_label = ttk.Label(main_frame, text=message)
        self.message_label.pack(pady=(0, 15))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var,
                                          maximum=100, length=300)
        self.progress_bar.pack(pady=(0, 15))
        
        # Cancel button
        self.cancel_button = ttk.Button(main_frame, text="Cancel", command=self.on_cancel)
        self.cancel_button.pack()
        
    def update_progress(self, value, message=None):
        """Update progress bar and message."""
        self.progress_var.set(value)
        if message:
            self.message_label.config(text=message)
        self.dialog.update()
        
    def on_cancel(self):
        """Handle cancel button click."""
        self.cancelled = True
        self.dialog.destroy()
        
    def is_cancelled(self):
        """Check if dialog was cancelled."""
        return self.cancelled
        
    def close(self):
        """Close the dialog."""
        self.dialog.destroy()


class SettingsDialog:
    """Advanced settings dialog."""
    
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Advanced Settings")
        self.dialog.geometry("500x400")
        self.dialog.resizable(True, True)
        
        # Center the dialog
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Create widgets
        self.setup_widgets()
        
        # Configure closing behavior
        self.dialog.protocol("WM_DELETE_WINDOW", self.on_cancel)
        
    def setup_widgets(self):
        """Setup dialog widgets."""
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Advanced Settings",
                               font=("Segoe UI", 14, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Notebook for different setting categories
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill="both", expand=True, pady=(0, 20))
        
        # Network settings tab
        self.setup_network_tab(notebook)
        
        # Scraping settings tab
        self.setup_scraping_tab(notebook)
        
        # Export settings tab
        self.setup_export_tab(notebook)
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill="x")
        
        ttk.Button(buttons_frame, text="OK", command=self.on_ok).pack(side="right", padx=(10, 0))
        ttk.Button(buttons_frame, text="Cancel", command=self.on_cancel).pack(side="right")
        ttk.Button(buttons_frame, text="Apply", command=self.on_apply).pack(side="right", padx=(0, 10))
        
    def setup_network_tab(self, notebook):
        """Setup network settings tab."""
        network_frame = ttk.Frame(notebook, padding=15)
        notebook.add(network_frame, text="Network")
        
        # HTTP headers
        headers_frame = ttk.LabelFrame(network_frame, text="HTTP Headers", padding=10)
        headers_frame.pack(fill="x", pady=(0, 15))
        
        ttk.Label(headers_frame, text="Accept-Language:").pack(anchor="w")
        self.accept_lang_var = tk.StringVar(value="en-US,en;q=0.9")
        ttk.Entry(headers_frame, textvariable=self.accept_lang_var, width=40).pack(fill="x", pady=(5, 10))
        
        ttk.Label(headers_frame, text="Accept-Encoding:").pack(anchor="w")
        self.accept_encoding_var = tk.StringVar(value="gzip, deflate, br")
        ttk.Entry(headers_frame, textvariable=self.accept_encoding_var, width=40).pack(fill="x", pady=(5, 0))
        
        # Proxy settings
        proxy_frame = ttk.LabelFrame(network_frame, text="Proxy Settings", padding=10)
        proxy_frame.pack(fill="x")
        
        self.use_proxy_var = tk.BooleanVar()
        ttk.Checkbutton(proxy_frame, text="Use Proxy", variable=self.use_proxy_var,
                       command=self.toggle_proxy).pack(anchor="w", pady=(0, 10))
        
        self.proxy_frame = ttk.Frame(proxy_frame)
        self.proxy_frame.pack(fill="x")
        
        ttk.Label(self.proxy_frame, text="Proxy URL:").pack(anchor="w")
        self.proxy_url_var = tk.StringVar()
        self.proxy_entry = ttk.Entry(self.proxy_frame, textvariable=self.proxy_url_var, width=40)
        self.proxy_entry.pack(fill="x", pady=(5, 0))
        self.proxy_entry.config(state="disabled")
        
    def setup_scraping_tab(self, notebook):
        """Setup scraping settings tab."""
        scraping_frame = ttk.Frame(notebook, padding=15)
        notebook.add(scraping_frame, text="Scraping")
        
        # Rate limiting
        rate_frame = ttk.LabelFrame(scraping_frame, text="Rate Limiting", padding=10)
        rate_frame.pack(fill="x", pady=(0, 15))
        
        ttk.Label(rate_frame, text="Requests per minute:").pack(anchor="w")
        self.requests_per_minute_var = tk.StringVar(value="30")
        ttk.Spinbox(rate_frame, from_=1, to=300, textvariable=self.requests_per_minute_var, width=10).pack(anchor="w", pady=(5, 10))
        
        ttk.Label(rate_frame, text="Random delay range (seconds):").pack(anchor="w")
        delay_frame = ttk.Frame(rate_frame)
        delay_frame.pack(fill="x", pady=(5, 0))
        
        ttk.Label(delay_frame, text="Min:").pack(side="left")
        self.min_delay_var = tk.StringVar(value="0.5")
        ttk.Entry(delay_frame, textvariable=self.min_delay_var, width=8).pack(side="left", padx=(5, 10))
        
        ttk.Label(delay_frame, text="Max:").pack(side="left")
        self.max_delay_var = tk.StringVar(value="2.0")
        ttk.Entry(delay_frame, textvariable=self.max_delay_var, width=8).pack(side="left", padx=(5, 0))
        
        # Error handling
        error_frame = ttk.LabelFrame(scraping_frame, text="Error Handling", padding=10)
        error_frame.pack(fill="x")
        
        self.skip_errors_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(error_frame, text="Skip products with errors", 
                       variable=self.skip_errors_var).pack(anchor="w", pady=(0, 10))
        
        self.log_errors_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(error_frame, text="Log all errors", 
                       variable=self.log_errors_var).pack(anchor="w")
        
    def setup_export_tab(self, notebook):
        """Setup export settings tab."""
        export_frame = ttk.Frame(notebook, padding=15)
        notebook.add(export_frame, text="Export")
        
        # CSV settings
        csv_frame = ttk.LabelFrame(export_frame, text="CSV Export Options", padding=10)
        csv_frame.pack(fill="x", pady=(0, 15))
        
        ttk.Label(csv_frame, text="Delimiter:").pack(anchor="w")
        self.csv_delimiter_var = tk.StringVar(value=",")
        delim_combo = ttk.Combobox(csv_frame, textvariable=self.csv_delimiter_var,
                                  values=[",", ";", "\t", "|"], width=10)
        delim_combo.pack(anchor="w", pady=(5, 10))
        
        self.include_headers_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(csv_frame, text="Include column headers", 
                       variable=self.include_headers_var).pack(anchor="w")
        
        # Date format
        date_frame = ttk.LabelFrame(export_frame, text="Date Format", padding=10)
        date_frame.pack(fill="x")
        
        ttk.Label(date_frame, text="Date format string:").pack(anchor="w")
        self.date_format_var = tk.StringVar(value="%Y-%m-%d %H:%M:%S")
        ttk.Entry(date_frame, textvariable=self.date_format_var, width=30).pack(anchor="w", pady=(5, 0))
        
    def toggle_proxy(self):
        """Toggle proxy settings availability."""
        if self.use_proxy_var.get():
            self.proxy_entry.config(state="normal")
        else:
            self.proxy_entry.config(state="disabled")
            
    def on_ok(self):
        """Handle OK button click."""
        self.apply_settings()
        self.result = "ok"
        self.dialog.destroy()
        
    def on_cancel(self):
        """Handle Cancel button click."""
        self.result = "cancel"
        self.dialog.destroy()
        
    def on_apply(self):
        """Handle Apply button click."""
        self.apply_settings()
        messagebox.showinfo("Settings", "Settings applied successfully!")
        
    def apply_settings(self):
        """Apply the settings to configuration."""
        settings = {
            'accept_language': self.accept_lang_var.get(),
            'accept_encoding': self.accept_encoding_var.get(),
            'use_proxy': self.use_proxy_var.get(),
            'proxy_url': self.proxy_url_var.get() if self.use_proxy_var.get() else None,
            'requests_per_minute': int(self.requests_per_minute_var.get()),
            'min_delay': float(self.min_delay_var.get()),
            'max_delay': float(self.max_delay_var.get()),
            'skip_errors': self.skip_errors_var.get(),
            'log_errors': self.log_errors_var.get(),
            'csv_delimiter': self.csv_delimiter_var.get(),
            'include_headers': self.include_headers_var.get(),
            'date_format': self.date_format_var.get()
        }
        
        self.config.update_advanced_settings(settings)
        
    def show(self):
        """Show the dialog and return result."""
        self.dialog.wait_window()
        return self.result


class ErrorDialog:
    """Error dialog with detailed error information and logging options."""
    
    def __init__(self, parent, title="Error", error_message="", detailed_error=""):
        self.parent = parent
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("600x400")
        self.dialog.resizable(True, True)
        
        # Center the dialog
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Create widgets
        self.setup_widgets(error_message, detailed_error)
        
    def setup_widgets(self, error_message, detailed_error):
        """Setup dialog widgets."""
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Error icon and message
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill="x", pady=(0, 15))
        
        # Error message
        ttk.Label(header_frame, text=error_message, font=("Segoe UI", 12)).pack(anchor="w")
        
        # Detailed error (expandable)
        if detailed_error:
            details_frame = ttk.LabelFrame(main_frame, text="Error Details", padding=10)
            details_frame.pack(fill="both", expand=True, pady=(0, 15))
            
            # Text widget with scrollbar
            text_frame = ttk.Frame(details_frame)
            text_frame.pack(fill="both", expand=True)
            
            error_text = tk.Text(text_frame, height=15, font=("Courier", 9))
            scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=error_text.yview)
            error_text.configure(yscrollcommand=scrollbar.set)
            
            error_text.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            error_text.insert(tk.END, detailed_error)
            error_text.config(state="disabled")
        
        # Buttons
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill="x")
        
        ttk.Button(buttons_frame, text="OK", command=self.dialog.destroy).pack(side="right")
        
        if detailed_error:
            ttk.Button(buttons_frame, text="Copy to Clipboard", 
                      command=lambda: self.copy_to_clipboard(detailed_error)).pack(side="right", padx=(0, 10))
        
    def copy_to_clipboard(self, text):
        """Copy error details to clipboard."""
        self.dialog.clipboard_clear()
        self.dialog.clipboard_append(text)
        messagebox.showinfo("Copied", "Error details copied to clipboard!")
        
    def show(self):
        """Show the dialog."""
        self.dialog.wait_window()
