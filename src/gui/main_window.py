"""
Main Window GUI for E-Commerce Data Scraper
Professional desktop interface with modern design and comprehensive functionality.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import os
from datetime import datetime
import pandas as pd

from utils.logger import get_logger
from scraper.scraper_engine import ScraperEngine
from data.exporter import DataExporter
from visualization.chart_generator import ChartGenerator
from gui.dialogs import ProgressDialog, SettingsDialog
from gui.themes import ThemeManager, ThemedWidget, configure_ttk_style
from gui.theme_dialog import ThemeDialog


class MainWindow:
    """Main application window with professional interface."""
    
    def __init__(self, root, config):
        self.root = root
        self.config = config
        self.logger = get_logger(__name__)
        self.scraped_data = pd.DataFrame()
        
        # Initialize theme manager
        self.theme_manager = ThemeManager()
        self.themed_widget = ThemedWidget(self.theme_manager)
        
        # Load theme preference from config
        saved_theme = self.config.get_setting("appearance", "theme", "light")
        if saved_theme:
            self.theme_manager.set_theme(saved_theme)
        
        # Initialize components
        self.scraper_engine = ScraperEngine(config)
        self.data_exporter = DataExporter()
        self.chart_generator = ChartGenerator()
        
        self.setup_window()
        self.create_widgets()
        self.setup_styles()
        self.apply_theme()
        
    def setup_window(self):
        """Configure the main window properties."""
        self.root.title("E-Commerce Data Scraper - Professional Edition")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - self.root.winfo_width()) // 2
        y = (self.root.winfo_screenheight() - self.root.winfo_height()) // 2
        self.root.geometry(f"+{x}+{y}")
        
        # Configure window icon (if available)
        try:
            icon_path = os.path.join("assets", "icon.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass
            
        # Configure window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_styles(self):
        """Configure custom styles for the application."""
        style = ttk.Style()
        
        # Configure modern theme
        if "clam" in style.theme_names():
            style.theme_use("clam")
        
        # Custom button styles
        style.configure("Action.TButton", 
                       font=("Segoe UI", 10, "bold"),
                       padding=(10, 5))
        
        style.configure("Success.TButton",
                       font=("Segoe UI", 9),
                       foreground="green")
        
        style.configure("Warning.TButton",
                       font=("Segoe UI", 9),
                       foreground="orange")
        
    def create_widgets(self):
        """Create and arrange all GUI widgets."""
        # Create main notebook for tabbed interface
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_scraping_tab()
        self.create_data_tab()
        self.create_visualization_tab()
        self.create_settings_tab()
        
        # Create status bar
        self.create_status_bar()
        
    def create_scraping_tab(self):
        """Create the web scraping configuration tab."""
        scraping_frame = ttk.Frame(self.notebook)
        self.notebook.add(scraping_frame, text="Web Scraping")
        
        # Main container with padding
        main_container = ttk.Frame(scraping_frame)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_container, 
                               text="E-Commerce Data Scraping Configuration",
                               font=("Segoe UI", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Site selection frame
        site_frame = ttk.LabelFrame(main_container, text="Target Website", padding=15)
        site_frame.pack(fill="x", pady=(0, 15))
        
        # Site selection
        ttk.Label(site_frame, text="Select Website:").pack(anchor="w")
        self.site_var = tk.StringVar()
        self.site_combo = ttk.Combobox(site_frame, textvariable=self.site_var,
                                      values=list(self.config.get_available_sites().keys()),
                                      state="readonly", width=40)
        self.site_combo.pack(pady=(5, 10), anchor="w")
        self.site_combo.bind("<<ComboboxSelected>>", self.on_site_selected)
        
        # Site info
        self.site_info_label = ttk.Label(site_frame, text="Select a website to see details",
                                        foreground="gray")
        self.site_info_label.pack(anchor="w")
        
        # Scraping parameters frame
        params_frame = ttk.LabelFrame(main_container, text="Scraping Parameters", padding=15)
        params_frame.pack(fill="x", pady=(0, 15))
        
        # Parameters grid
        params_grid = ttk.Frame(params_frame)
        params_grid.pack(fill="x")
        
        # Max products
        ttk.Label(params_grid, text="Max Products:").grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.max_products_var = tk.StringVar(value="50")
        max_products_spin = ttk.Spinbox(params_grid, from_=1, to=1000, 
                                       textvariable=self.max_products_var, width=10)
        max_products_spin.grid(row=0, column=1, sticky="w")
        
        # Delay between requests
        ttk.Label(params_grid, text="Delay (seconds):").grid(row=0, column=2, sticky="w", padx=(20, 10))
        self.delay_var = tk.StringVar(value="1.0")
        delay_spin = ttk.Spinbox(params_grid, from_=0.5, to=10.0, increment=0.5,
                                textvariable=self.delay_var, width=10)
        delay_spin.grid(row=0, column=3, sticky="w")
        
        # Category filter
        ttk.Label(params_grid, text="Category Filter:").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=(10, 0))
        self.category_var = tk.StringVar()
        category_entry = ttk.Entry(params_grid, textvariable=self.category_var, width=30)
        category_entry.grid(row=1, column=1, columnspan=3, sticky="w", pady=(10, 0))
        
        # Control buttons frame
        controls_frame = ttk.Frame(main_container)
        controls_frame.pack(fill="x", pady=15)
        
        # Start scraping button
        self.start_button = ttk.Button(controls_frame, text="Start Scraping",
                                      style="Action.TButton",
                                      command=self.start_scraping)
        self.start_button.pack(side="left", padx=(0, 10))
        
        # Stop scraping button
        self.stop_button = ttk.Button(controls_frame, text="Stop Scraping",
                                     command=self.stop_scraping, state="disabled")
        self.stop_button.pack(side="left", padx=(0, 10))
        
        # Progress frame
        progress_frame = ttk.LabelFrame(main_container, text="Scraping Progress", padding=15)
        progress_frame.pack(fill="x", pady=(0, 15))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var,
                                          maximum=100, length=400)
        self.progress_bar.pack(pady=(0, 10))
        
        # Status label
        self.status_label = ttk.Label(progress_frame, text="Ready to start scraping")
        self.status_label.pack()
        
        # Results preview frame
        results_frame = ttk.LabelFrame(main_container, text="Results Preview", padding=15)
        results_frame.pack(fill="both", expand=True)
        
        # Results tree
        columns = ("Product Name", "Price", "Rating", "URL")
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=200)
        
        # Scrollbars for results tree
        tree_scroll_y = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_tree.yview)
        tree_scroll_x = ttk.Scrollbar(results_frame, orient="horizontal", command=self.results_tree.xview)
        self.results_tree.configure(yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)
        
        self.results_tree.pack(side="left", fill="both", expand=True)
        tree_scroll_y.pack(side="right", fill="y")
        tree_scroll_x.pack(side="bottom", fill="x")
        
    def create_data_tab(self):
        """Create the data management and export tab."""
        data_frame = ttk.Frame(self.notebook)
        self.notebook.add(data_frame, text="Data Management")
        
        main_container = ttk.Frame(data_frame)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_container, 
                               text="Data Management & Export",
                               font=("Segoe UI", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Data summary frame
        summary_frame = ttk.LabelFrame(main_container, text="Data Summary", padding=15)
        summary_frame.pack(fill="x", pady=(0, 15))
        
        self.data_summary_label = ttk.Label(summary_frame, text="No data loaded")
        self.data_summary_label.pack()
        
        # Export options frame
        export_frame = ttk.LabelFrame(main_container, text="Export Options", padding=15)
        export_frame.pack(fill="x", pady=(0, 15))
        
        # Export format selection
        format_frame = ttk.Frame(export_frame)
        format_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(format_frame, text="Export Format:").pack(side="left")
        self.export_format_var = tk.StringVar(value="CSV")
        formats = ["CSV", "Excel", "JSON"]
        for fmt in formats:
            ttk.Radiobutton(format_frame, text=fmt, variable=self.export_format_var,
                           value=fmt).pack(side="left", padx=10)
        
        # Export buttons
        export_buttons_frame = ttk.Frame(export_frame)
        export_buttons_frame.pack(fill="x")
        
        ttk.Button(export_buttons_frame, text="Export All Data",
                  command=self.export_all_data).pack(side="left", padx=(0, 10))
        
        ttk.Button(export_buttons_frame, text="Export Selected",
                  command=self.export_selected_data).pack(side="left", padx=(0, 10))
        
        # Data filtering frame
        filter_frame = ttk.LabelFrame(main_container, text="Data Filtering", padding=15)
        filter_frame.pack(fill="x", pady=(0, 15))
        
        # Price range filter
        price_frame = ttk.Frame(filter_frame)
        price_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(price_frame, text="Price Range:").pack(side="left")
        ttk.Label(price_frame, text="Min:").pack(side="left", padx=(20, 5))
        self.min_price_var = tk.StringVar()
        ttk.Entry(price_frame, textvariable=self.min_price_var, width=10).pack(side="left")
        
        ttk.Label(price_frame, text="Max:").pack(side="left", padx=(10, 5))
        self.max_price_var = tk.StringVar()
        ttk.Entry(price_frame, textvariable=self.max_price_var, width=10).pack(side="left")
        
        # Rating filter
        rating_frame = ttk.Frame(filter_frame)
        rating_frame.pack(fill="x")
        
        ttk.Label(rating_frame, text="Minimum Rating:").pack(side="left")
        self.min_rating_var = tk.StringVar(value="0")
        ttk.Spinbox(rating_frame, from_=0, to=5, increment=0.1,
                   textvariable=self.min_rating_var, width=10).pack(side="left", padx=(20, 0))
        
        ttk.Button(rating_frame, text="Apply Filters",
                  command=self.apply_filters).pack(side="right")
        
    def create_visualization_tab(self):
        """Create the data visualization tab."""
        viz_frame = ttk.Frame(self.notebook)
        self.notebook.add(viz_frame, text="Visualization")
        
        main_container = ttk.Frame(viz_frame)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_container, 
                               text="Data Visualization & Analytics",
                               font=("Segoe UI", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Chart type selection
        chart_frame = ttk.LabelFrame(main_container, text="Chart Options", padding=15)
        chart_frame.pack(fill="x", pady=(0, 15))
        
        # Chart type
        type_frame = ttk.Frame(chart_frame)
        type_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(type_frame, text="Chart Type:").pack(side="left")
        self.chart_type_var = tk.StringVar(value="histogram")
        chart_types = [("Price Distribution", "histogram"), 
                      ("Rating vs Price", "scatter"),
                      ("Top Products", "bar"),
                      ("Price Range Analysis", "box")]
        
        for text, value in chart_types:
            ttk.Radiobutton(type_frame, text=text, variable=self.chart_type_var,
                           value=value).pack(side="left", padx=10)
        
        # Generate chart button
        ttk.Button(chart_frame, text="Generate Chart",
                  style="Action.TButton",
                  command=self.generate_chart).pack(pady=10)
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(main_container, text="Data Statistics", padding=15)
        stats_frame.pack(fill="both", expand=True)
        
        # Statistics text widget
        self.stats_text = tk.Text(stats_frame, height=15, font=("Courier", 10))
        stats_scroll = ttk.Scrollbar(stats_frame, orient="vertical", command=self.stats_text.yview)
        self.stats_text.configure(yscrollcommand=stats_scroll.set)
        
        self.stats_text.pack(side="left", fill="both", expand=True)
        stats_scroll.pack(side="right", fill="y")
        
        # Update statistics button
        ttk.Button(main_container, text="Update Statistics",
                  command=self.update_statistics).pack(pady=10)
        
    def create_settings_tab(self):
        """Create the settings and configuration tab."""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="Settings")
        
        main_container = ttk.Frame(settings_frame)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_container, 
                               text="Application Settings",
                               font=("Segoe UI", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # General settings
        general_frame = ttk.LabelFrame(main_container, text="General Settings", padding=15)
        general_frame.pack(fill="x", pady=(0, 15))
        
        # User agent
        ttk.Label(general_frame, text="User Agent:").pack(anchor="w")
        self.user_agent_var = tk.StringVar(value=self.config.get_user_agent())
        user_agent_entry = ttk.Entry(general_frame, textvariable=self.user_agent_var, width=80)
        user_agent_entry.pack(fill="x", pady=(5, 10))
        
        # Logging level
        log_frame = ttk.Frame(general_frame)
        log_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(log_frame, text="Logging Level:").pack(side="left")
        self.log_level_var = tk.StringVar(value="INFO")
        log_combo = ttk.Combobox(log_frame, textvariable=self.log_level_var,
                                values=["DEBUG", "INFO", "WARNING", "ERROR"],
                                state="readonly", width=15)
        log_combo.pack(side="left", padx=(10, 0))
        
        # Network settings
        network_frame = ttk.LabelFrame(main_container, text="Network Settings", padding=15)
        network_frame.pack(fill="x", pady=(0, 15))
        
        # Timeout
        timeout_frame = ttk.Frame(network_frame)
        timeout_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(timeout_frame, text="Request Timeout (seconds):").pack(side="left")
        self.timeout_var = tk.StringVar(value="30")
        ttk.Spinbox(timeout_frame, from_=5, to=120, textvariable=self.timeout_var, width=10).pack(side="left", padx=(10, 0))
        
        # Retry attempts
        retry_frame = ttk.Frame(network_frame)
        retry_frame.pack(fill="x")
        
        ttk.Label(retry_frame, text="Max Retry Attempts:").pack(side="left")
        self.retry_var = tk.StringVar(value="3")
        ttk.Spinbox(retry_frame, from_=1, to=10, textvariable=self.retry_var, width=10).pack(side="left", padx=(10, 0))
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_container)
        buttons_frame.pack(fill="x", pady=20)
        
        ttk.Button(buttons_frame, text="Save Settings",
                  style="Success.TButton",
                  command=self.save_settings).pack(side="left", padx=(0, 10))
        
        ttk.Button(buttons_frame, text="Reset to Defaults",
                  style="Warning.TButton",
                  command=self.reset_settings).pack(side="left")
        
    def create_status_bar(self):
        """Create the status bar at the bottom of the window."""
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(side="bottom", fill="x", padx=5, pady=5)
        
        self.status_text = ttk.Label(self.status_frame, text="Ready")
        self.status_text.pack(side="left")
        
        # Progress indicator for status bar
        self.status_progress = ttk.Progressbar(self.status_frame, length=100, mode="indeterminate")
        self.status_progress.pack(side="right", padx=(10, 0))
        
    def on_site_selected(self, event=None):
        """Handle site selection change."""
        site_name = self.site_var.get()
        if site_name:
            site_info = self.config.get_site_info(site_name)
            info_text = f"URL: {site_info.get('base_url', 'N/A')}\nDescription: {site_info.get('description', 'N/A')}"
            self.site_info_label.config(text=info_text, foreground="black")
        
    def start_scraping(self):
        """Start the web scraping process."""
        site_name = self.site_var.get()
        if not site_name:
            messagebox.showwarning("Warning", "Please select a website to scrape.")
            return
        
        try:
            max_products = int(self.max_products_var.get())
            delay = float(self.delay_var.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for parameters.")
            return
        
        # Update UI state
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.progress_var.set(0)
        self.status_label.config(text="Initializing scraper...")
        self.status_progress.start()
        
        # Clear previous results
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Start scraping in separate thread
        self.scraping_thread = threading.Thread(
            target=self._scraping_worker,
            args=(site_name, max_products, delay, self.category_var.get()),
            daemon=True
        )
        self.scraping_active = True
        self.scraping_thread.start()
        
    def _scraping_worker(self, site_name, max_products, delay, category_filter):
        """Worker thread for web scraping."""
        try:
            self.logger.info(f"Starting scraping for {site_name}")
            
            # Configure scraper
            scraper_config = {
                'max_products': max_products,
                'delay': delay,
                'category_filter': category_filter
            }
            
            # Start scraping with progress callback
            results = self.scraper_engine.scrape_site(
                site_name, 
                scraper_config, 
                progress_callback=self.update_scraping_progress
            )
            
            if results is not None and not results.empty:
                self.scraped_data = results
                self.root.after(0, self.on_scraping_complete, results)
            else:
                self.root.after(0, self.on_scraping_error, "No data was scraped")
                
        except Exception as e:
            self.logger.error(f"Scraping error: {str(e)}")
            self.root.after(0, self.on_scraping_error, str(e))
        
    def update_scraping_progress(self, current, total, status=""):
        """Update scraping progress from worker thread."""
        if self.scraping_active:
            progress = (current / total) * 100 if total > 0 else 0
            self.root.after(0, self._update_progress_ui, progress, status)
        
    def _update_progress_ui(self, progress, status):
        """Update progress UI elements."""
        self.progress_var.set(progress)
        if status:
            self.status_label.config(text=status)
        
    def on_scraping_complete(self, results):
        """Handle successful scraping completion."""
        self.scraping_active = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.status_progress.stop()
        self.progress_var.set(100)
        self.status_label.config(text=f"Scraping completed. {len(results)} products found.")
        
        # Update results tree
        for _, row in results.iterrows():
            self.results_tree.insert("", "end", values=(
                row.get('name', 'N/A'),
                row.get('price', 'N/A'),
                row.get('rating', 'N/A'),
                row.get('url', 'N/A')
            ))
        
        # Update data summary
        self.update_data_summary()
        
        messagebox.showinfo("Success", f"Scraping completed successfully!\n{len(results)} products scraped.")
        
    def on_scraping_error(self, error_msg):
        """Handle scraping errors."""
        self.scraping_active = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.status_progress.stop()
        self.status_label.config(text=f"Scraping failed: {error_msg}")
        
        messagebox.showerror("Scraping Error", f"Failed to scrape data:\n{error_msg}")
        
    def stop_scraping(self):
        """Stop the scraping process."""
        self.scraping_active = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.status_progress.stop()
        self.status_label.config(text="Scraping stopped by user.")
        
    def update_data_summary(self):
        """Update the data summary display."""
        if self.scraped_data.empty:
            self.data_summary_label.config(text="No data loaded")
            return
        
        total_products = len(self.scraped_data)
        price_col = 'price'
        rating_col = 'rating'
        
        summary_text = f"Total Products: {total_products}"
        
        if price_col in self.scraped_data.columns:
            # Convert price column to numeric, handling currency symbols
            price_series = pd.to_numeric(
                self.scraped_data[price_col].astype(str).str.replace(r'[^\d.]', '', regex=True),
                errors='coerce'
            )
            if not price_series.isna().all():
                avg_price = price_series.mean()
                min_price = price_series.min()
                max_price = price_series.max()
                summary_text += f"\nPrice Range: ${min_price:.2f} - ${max_price:.2f}\nAverage Price: ${avg_price:.2f}"
        
        if rating_col in self.scraped_data.columns:
            rating_series = pd.to_numeric(self.scraped_data[rating_col], errors='coerce')
            if not rating_series.isna().all():
                avg_rating = rating_series.mean()
                summary_text += f"\nAverage Rating: {avg_rating:.2f}/5"
        
        self.data_summary_label.config(text=summary_text)
        
    def export_all_data(self):
        """Export all scraped data."""
        if self.scraped_data.empty:
            messagebox.showwarning("Warning", "No data to export.")
            return
        
        self._export_data(self.scraped_data)
        
    def export_selected_data(self):
        """Export selected data from the results tree."""
        selected_items = self.results_tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "No data selected for export.")
            return
        
        # Create DataFrame from selected items
        selected_data = []
        for item in selected_items:
            values = self.results_tree.item(item, 'values')
            selected_data.append({
                'name': values[0],
                'price': values[1],
                'rating': values[2],
                'url': values[3]
            })
        
        selected_df = pd.DataFrame(selected_data)
        self._export_data(selected_df)
        
    def _export_data(self, data):
        """Export data to specified format."""
        export_format = self.export_format_var.get()
        
        # Get file path from user
        file_types = {
            'CSV': [('CSV files', '*.csv')],
            'Excel': [('Excel files', '*.xlsx')],
            'JSON': [('JSON files', '*.json')]
        }
        
        filename = filedialog.asksaveasfilename(
            defaultextension=f".{export_format.lower()}",
            filetypes=file_types[export_format]
        )
        
        if filename:
            try:
                success = self.data_exporter.export_data(data, filename, export_format.lower())
                if success:
                    messagebox.showinfo("Success", f"Data exported successfully to {filename}")
                else:
                    messagebox.showerror("Error", "Failed to export data")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {str(e)}")
                
    def apply_filters(self):
        """Apply data filters and update display."""
        if self.scraped_data.empty:
            messagebox.showwarning("Warning", "No data to filter.")
            return
        
        filtered_data = self.scraped_data.copy()
        
        # Apply price filters
        min_price = self.min_price_var.get()
        max_price = self.max_price_var.get()
        
        if min_price or max_price:
            price_series = pd.to_numeric(
                filtered_data['price'].astype(str).str.replace(r'[^\d.]', '', regex=True),
                errors='coerce'
            )
            
            if min_price:
                try:
                    min_val = float(min_price)
                    filtered_data = filtered_data[price_series >= min_val]
                except ValueError:
                    pass
            
            if max_price:
                try:
                    max_val = float(max_price)
                    filtered_data = filtered_data[price_series <= max_val]
                except ValueError:
                    pass
        
        # Apply rating filter
        min_rating = self.min_rating_var.get()
        if min_rating:
            try:
                min_rating_val = float(min_rating)
                rating_series = pd.to_numeric(filtered_data['rating'], errors='coerce')
                filtered_data = filtered_data[rating_series >= min_rating_val]
            except ValueError:
                pass
        
        # Update results tree
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        for _, row in filtered_data.iterrows():
            self.results_tree.insert("", "end", values=(
                row.get('name', 'N/A'),
                row.get('price', 'N/A'),
                row.get('rating', 'N/A'),
                row.get('url', 'N/A')
            ))
        
        messagebox.showinfo("Filter Applied", f"Showing {len(filtered_data)} products after filtering.")
        
    def generate_chart(self):
        """Generate visualization chart."""
        if self.scraped_data.empty:
            messagebox.showwarning("Warning", "No data available for visualization.")
            return
        
        chart_type = self.chart_type_var.get()
        
        try:
            self.chart_generator.generate_chart(self.scraped_data, chart_type)
            messagebox.showinfo("Success", "Chart generated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate chart: {str(e)}")
            
    def update_statistics(self):
        """Update and display data statistics."""
        if self.scraped_data.empty:
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(tk.END, "No data available for statistics.")
            return
        
        try:
            stats = self.chart_generator.generate_statistics(self.scraped_data)
            
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(tk.END, stats)
        except Exception as e:
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(tk.END, f"Error generating statistics: {str(e)}")
            
    def save_settings(self):
        """Save current settings."""
        try:
            self.config.update_settings({
                'user_agent': self.user_agent_var.get(),
                'log_level': self.log_level_var.get(),
                'timeout': int(self.timeout_var.get()),
                'retry_attempts': int(self.retry_var.get())
            })
            messagebox.showinfo("Success", "Settings saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
            
    def reset_settings(self):
        """Reset settings to defaults."""
        if messagebox.askyesno("Confirm Reset", "Reset all settings to defaults?"):
            self.config.reset_to_defaults()
            # Update UI with default values
            self.user_agent_var.set(self.config.get_user_agent())
            self.log_level_var.set("INFO")
            self.timeout_var.set("30")
            self.retry_var.set("3")
            messagebox.showinfo("Success", "Settings reset to defaults!")
            
    def apply_theme(self):
        """Apply current theme to all widgets."""
        try:
            # Configure ttk style
            configure_ttk_style(self.theme_manager)
            
            # Apply theme to root window
            self.root.configure(bg=self.theme_manager.get_color("bg_primary"))
            
            # Apply theme to main frames
            if hasattr(self, 'main_frame'):
                self.themed_widget.apply_theme(self.main_frame, "frame")
            
            # Apply theme to notebook and tabs
            if hasattr(self, 'notebook'):
                style = ttk.Style()
                colors = self.theme_manager.get_colors()
                
                # Update notebook style
                style.configure("TNotebook", 
                               background=colors.get("bg_primary"))
                
                style.configure("TNotebook.Tab",
                               background=colors.get("tab_normal"),
                               foreground=colors.get("text_primary"))
                
                style.map("TNotebook.Tab",
                         background=[("selected", colors.get("tab_selected")),
                                   ("active", colors.get("tab_hover"))],
                         foreground=[("selected", colors.get("text_inverse")),
                                   ("active", colors.get("text_primary"))])
            
            # Apply theme to all tab content
            self._apply_theme_to_tabs()
            
            # Update status bar
            if hasattr(self, 'status_bar'):
                self.themed_widget.apply_theme(self.status_bar, "frame_secondary")
                if hasattr(self, 'status_label'):
                    self.themed_widget.apply_theme(self.status_label, "label_secondary")
            
            self.logger.info(f"Applied theme: {self.theme_manager.get_current_theme()}")
            
        except Exception as e:
            self.logger.error(f"Error applying theme: {e}")
    
    def _apply_theme_to_tabs(self):
        """Apply theme to all tab contents."""
        try:
            # Scraping tab
            if hasattr(self, 'scraping_frame'):
                self._apply_theme_to_scraping_tab()
            
            # Data tab
            if hasattr(self, 'data_frame'):
                self._apply_theme_to_data_tab()
                
            # Visualization tab
            if hasattr(self, 'viz_frame'):
                self._apply_theme_to_visualization_tab()
                
            # Settings tab
            if hasattr(self, 'settings_frame'):
                self._apply_theme_to_settings_tab()
                
        except Exception as e:
            self.logger.error(f"Error applying theme to tabs: {e}")
    
    def _apply_theme_to_scraping_tab(self):
        """Apply theme to scraping tab widgets."""
        try:
            self.themed_widget.apply_theme(self.scraping_frame, "frame")
            
            # Apply to all child widgets recursively
            self._apply_theme_recursive(self.scraping_frame)
            
        except Exception as e:
            self.logger.error(f"Error applying theme to scraping tab: {e}")
    
    def _apply_theme_to_data_tab(self):
        """Apply theme to data management tab widgets."""
        try:
            self.themed_widget.apply_theme(self.data_frame, "frame")
            
            # Apply to all child widgets recursively
            self._apply_theme_recursive(self.data_frame)
            
        except Exception as e:
            self.logger.error(f"Error applying theme to data tab: {e}")
    
    def _apply_theme_to_visualization_tab(self):
        """Apply theme to visualization tab widgets."""
        try:
            self.themed_widget.apply_theme(self.viz_frame, "frame")
            
            # Apply to all child widgets recursively
            self._apply_theme_recursive(self.viz_frame)
            
        except Exception as e:
            self.logger.error(f"Error applying theme to visualization tab: {e}")
    
    def _apply_theme_to_settings_tab(self):
        """Apply theme to settings tab widgets."""
        try:
            self.themed_widget.apply_theme(self.settings_frame, "frame")
            
            # Apply to all child widgets recursively
            self._apply_theme_recursive(self.settings_frame)
            
            # Add theme selection to settings tab if not already present
            self._add_theme_settings()
            
        except Exception as e:
            self.logger.error(f"Error applying theme to settings tab: {e}")
    
    def _apply_theme_recursive(self, widget):
        """Apply theme to widget and all its children recursively."""
        try:
            widget_class = widget.winfo_class()
            
            if widget_class == "Frame":
                self.themed_widget.apply_theme(widget, "frame")
            elif widget_class == "Label":
                self.themed_widget.apply_theme(widget, "label")
            elif widget_class == "Button":
                # Determine button type by text or configuration
                button_text = str(widget.cget("text")).lower()
                if any(word in button_text for word in ["start", "scrape", "export", "generate"]):
                    self.themed_widget.apply_theme(widget, "button_primary")
                else:
                    self.themed_widget.apply_theme(widget, "button_secondary")
            elif widget_class == "Entry":
                self.themed_widget.apply_theme(widget, "entry")
            elif widget_class == "Text":
                self.themed_widget.apply_theme(widget, "text")
            elif widget_class == "Listbox":
                self.themed_widget.apply_theme(widget, "listbox")
            
            # Apply to children
            for child in widget.winfo_children():
                if hasattr(child, 'winfo_class'):
                    self._apply_theme_recursive(child)
                    
        except Exception as e:
            # Silently continue if widget doesn't support certain operations
            pass
    
    def _add_theme_settings(self):
        """Add theme selection controls to settings tab."""
        try:
            if not hasattr(self, 'settings_frame'):
                return
                
            # Check if theme settings already exist
            for child in self.settings_frame.winfo_children():
                if hasattr(child, 'winfo_name') and 'theme' in str(child.winfo_name()):
                    return  # Theme settings already added
            
            # Create theme settings section
            theme_section = ttk.LabelFrame(self.settings_frame, text="Appearance", padding=10)
            theme_section.pack(fill=tk.X, padx=10, pady=5)
            
            # Theme selection
            theme_control_frame = ttk.Frame(theme_section)
            theme_control_frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(theme_control_frame, text="Theme:").pack(side=tk.LEFT, padx=(0, 10))
            
            # Theme dropdown
            self.theme_var = tk.StringVar(value=self.theme_manager.get_current_theme())
            theme_combo = ttk.Combobox(theme_control_frame, textvariable=self.theme_var,
                                     state="readonly", width=20)
            
            available_themes = self.theme_manager.get_available_themes()
            theme_combo['values'] = list(available_themes.keys())
            theme_combo.pack(side=tk.LEFT, padx=(0, 10))
            theme_combo.bind('<<ComboboxSelected>>', self.on_theme_changed)
            
            # Theme customization button
            theme_btn = ttk.Button(theme_control_frame, text="Customize Colors",
                                 command=self.open_theme_dialog)
            theme_btn.pack(side=tk.LEFT, padx=(10, 0))
            
            # Dark mode toggle (for convenience)
            dark_mode_frame = ttk.Frame(theme_section)
            dark_mode_frame.pack(fill=tk.X, pady=(5, 0))
            
            self.dark_mode_var = tk.BooleanVar(value=self.theme_manager.is_dark_theme())
            dark_mode_check = ttk.Checkbutton(dark_mode_frame, text="Dark Mode",
                                            variable=self.dark_mode_var,
                                            command=self.toggle_dark_mode)
            dark_mode_check.pack(side=tk.LEFT)
            
        except Exception as e:
            self.logger.error(f"Error adding theme settings: {e}")
    
    def on_theme_changed(self, event=None):
        """Handle theme selection change."""
        try:
            new_theme = self.theme_var.get()
            if self.theme_manager.set_theme(new_theme):
                # Save theme preference
                self.config.set_setting("appearance", "theme", new_theme)
                self.config.save_settings()
                
                # Update dark mode checkbox
                if hasattr(self, 'dark_mode_var'):
                    self.dark_mode_var.set(self.theme_manager.is_dark_theme())
                
                # Apply theme
                self.apply_theme()
                
                # Update chart generator with new theme
                if hasattr(self, 'chart_generator'):
                    self.chart_generator.set_theme_manager(self.theme_manager)
                
                self.logger.info(f"Theme changed to: {new_theme}")
                
        except Exception as e:
            self.logger.error(f"Error changing theme: {e}")
            messagebox.showerror("Theme Error", f"Failed to apply theme: {e}")
    
    def toggle_dark_mode(self):
        """Toggle between dark and light mode."""
        try:
            if self.dark_mode_var.get():
                # Switch to dark theme
                self.theme_manager.set_theme("dark")
                self.theme_var.set("dark")
            else:
                # Switch to light theme
                self.theme_manager.set_theme("light")
                self.theme_var.set("light")
            
            # Save preference and apply theme
            self.config.set_setting("appearance", "theme", self.theme_manager.get_current_theme())
            self.config.save_settings()
            self.apply_theme()
            
            # Update chart generator
            if hasattr(self, 'chart_generator'):
                self.chart_generator.set_theme_manager(self.theme_manager)
                
        except Exception as e:
            self.logger.error(f"Error toggling dark mode: {e}")
    
    def open_theme_dialog(self):
        """Open theme customization dialog."""
        try:
            dialog = ThemeDialog(self.root, self.theme_manager, self.apply_theme)
            result = dialog.show()
            
            if result:
                # Update theme selection
                self.theme_var.set(result)
                
                # Save preference
                self.config.set_setting("appearance", "theme", result)
                self.config.save_settings()
                
                # Update dark mode checkbox
                if hasattr(self, 'dark_mode_var'):
                    self.dark_mode_var.set(self.theme_manager.is_dark_theme())
                
                # Update chart generator
                if hasattr(self, 'chart_generator'):
                    self.chart_generator.set_theme_manager(self.theme_manager)
                    
                self.logger.info(f"Theme customized: {result}")
                
        except Exception as e:
            self.logger.error(f"Error opening theme dialog: {e}")
            messagebox.showerror("Theme Error", f"Failed to open theme dialog: {e}")

    def on_closing(self):
        """Handle application closing."""
        try:
            # Save current theme before closing
            current_theme = self.theme_manager.get_current_theme()
            self.config.set_setting("appearance", "theme", current_theme)
            self.config.save_settings()
            
        except Exception as e:
            self.logger.error(f"Error saving settings on close: {e}")
        
        if hasattr(self, 'scraping_active') and self.scraping_active:
            if messagebox.askyesno("Confirm Exit", "Scraping is in progress. Do you want to stop and exit?"):
                self.scraping_active = False
                self.root.destroy()
        else:
            self.root.destroy()
