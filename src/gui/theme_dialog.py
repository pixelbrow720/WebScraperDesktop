"""
Theme selection and customization dialog for E-Commerce Data Scraper.
Allows users to switch themes and customize colors.
"""

import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
from typing import Callable, Optional
from .themes import ThemeManager, ThemedWidget, configure_ttk_style


class ThemeDialog:
    """Dialog for theme selection and customization."""
    
    def __init__(self, parent, theme_manager: ThemeManager, apply_callback: Callable = None):
        self.parent = parent
        self.theme_manager = theme_manager
        self.apply_callback = apply_callback
        self.dialog = None
        self.result = None
        
        # Track original theme to allow cancellation
        self.original_theme = theme_manager.get_current_theme()
        
        # UI variables
        self.theme_var = tk.StringVar(value=theme_manager.get_current_theme())
        self.preview_frame = None
        self.color_buttons = {}
        
    def show(self) -> Optional[str]:
        """Show theme dialog and return selected theme."""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Theme Settings")
        self.dialog.geometry("600x500")
        self.dialog.resizable(True, True)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (500 // 2)
        self.dialog.geometry(f"600x500+{x}+{y}")
        
        self.setup_widgets()
        self.apply_current_theme()
        
        # Handle window close
        self.dialog.protocol("WM_DELETE_WINDOW", self.on_cancel)
        
        # Wait for dialog to close
        self.dialog.wait_window()
        
        return self.result
    
    def setup_widgets(self):
        """Setup dialog widgets."""
        # Main container
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Theme selection section
        self.create_theme_selection(main_frame)
        
        # Preview section
        self.create_preview_section(main_frame)
        
        # Custom theme section
        self.create_custom_theme_section(main_frame)
        
        # Buttons
        self.create_buttons(main_frame)
    
    def create_theme_selection(self, parent):
        """Create theme selection section."""
        # Theme selection frame
        theme_frame = ttk.LabelFrame(parent, text="Select Theme", padding=10)
        theme_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Theme selection
        ttk.Label(theme_frame, text="Theme:").pack(anchor=tk.W)
        
        theme_combo = ttk.Combobox(theme_frame, textvariable=self.theme_var, 
                                  state="readonly", width=30)
        
        # Populate themes
        available_themes = self.theme_manager.get_available_themes()
        theme_combo['values'] = list(available_themes.keys())
        theme_combo.pack(fill=tk.X, pady=(5, 0))
        
        # Bind theme change
        theme_combo.bind('<<ComboboxSelected>>', self.on_theme_changed)
        
        # Theme description
        self.theme_desc_label = ttk.Label(theme_frame, text="", foreground="gray")
        self.theme_desc_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Update description
        self.update_theme_description()
    
    def create_preview_section(self, parent):
        """Create theme preview section."""
        preview_frame = ttk.LabelFrame(parent, text="Preview", padding=10)
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Create preview widgets
        self.preview_frame = ttk.Frame(preview_frame)
        self.preview_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sample widgets for preview
        self.create_preview_widgets()
    
    def create_preview_widgets(self):
        """Create sample widgets for theme preview."""
        # Clear existing widgets
        for widget in self.preview_frame.winfo_children():
            widget.destroy()
        
        # Preview container
        container = tk.Frame(self.preview_frame)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Sample notebook
        notebook = ttk.Notebook(container)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1 - Basic widgets
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="Basic Widgets")
        
        # Sample frame with widgets
        sample_frame = tk.Frame(tab1)
        sample_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Sample labels
        title_label = tk.Label(sample_frame, text="Sample Application", 
                              font=("Arial", 14, "bold"))
        title_label.pack(anchor=tk.W, pady=(0, 10))
        
        subtitle_label = tk.Label(sample_frame, text="Theme Preview", 
                                 font=("Arial", 10))
        subtitle_label.pack(anchor=tk.W)
        
        # Sample buttons
        button_frame = tk.Frame(sample_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        primary_btn = tk.Button(button_frame, text="Primary Button", width=15)
        primary_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        secondary_btn = tk.Button(button_frame, text="Secondary", width=15)
        secondary_btn.pack(side=tk.LEFT, padx=5)
        
        # Sample entry
        entry_frame = tk.Frame(sample_frame)
        entry_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(entry_frame, text="Sample Input:").pack(anchor=tk.W)
        sample_entry = tk.Entry(entry_frame, width=30)
        sample_entry.pack(fill=tk.X, pady=(2, 0))
        sample_entry.insert(0, "Sample text content")
        
        # Sample text widget
        text_frame = tk.Frame(sample_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        tk.Label(text_frame, text="Sample Text Area:").pack(anchor=tk.W)
        sample_text = tk.Text(text_frame, height=6, width=50)
        sample_text.pack(fill=tk.BOTH, expand=True, pady=(2, 0))
        sample_text.insert(tk.END, "This is a sample text area showing how text content will appear in the selected theme.")
        
        # Tab 2 - Data display
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="Data Display")
        
        # Sample data display
        data_frame = tk.Frame(tab2)
        data_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Sample listbox
        list_frame = tk.Frame(data_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(list_frame, text="Sample Data List:").pack(anchor=tk.W)
        sample_listbox = tk.Listbox(list_frame, height=8)
        sample_listbox.pack(fill=tk.BOTH, expand=True, pady=(2, 0))
        
        # Add sample data
        sample_data = [
            "Product A - $29.99 - Rating: 4.5",
            "Product B - $19.99 - Rating: 4.2", 
            "Product C - $39.99 - Rating: 4.8",
            "Product D - $24.99 - Rating: 4.0",
            "Product E - $34.99 - Rating: 4.6"
        ]
        
        for item in sample_data:
            sample_listbox.insert(tk.END, item)
        
        # Store widgets for theming
        self.preview_widgets = {
            'container': container,
            'sample_frame': sample_frame,
            'title_label': title_label,
            'subtitle_label': subtitle_label,
            'button_frame': button_frame,
            'primary_btn': primary_btn,
            'secondary_btn': secondary_btn,
            'entry_frame': entry_frame,
            'sample_entry': sample_entry,
            'text_frame': text_frame,
            'sample_text': sample_text,
            'data_frame': data_frame,
            'list_frame': list_frame,
            'sample_listbox': sample_listbox
        }
    
    def create_custom_theme_section(self, parent):
        """Create custom theme editing section."""
        custom_frame = ttk.LabelFrame(parent, text="Custom Colors", padding=10)
        custom_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Color customization grid
        color_grid = tk.Frame(custom_frame)
        color_grid.pack(fill=tk.X)
        
        # Key color settings
        color_settings = [
            ("Background", "bg_primary"),
            ("Text", "text_primary"),
            ("Primary Button", "btn_primary"),
            ("Secondary Button", "btn_secondary"),
            ("Success", "success"),
            ("Warning", "warning"),
            ("Error", "error"),
            ("Selection", "selection")
        ]
        
        self.color_buttons = {}
        
        for i, (label, color_key) in enumerate(color_settings):
            row = i // 4
            col = (i % 4) * 2
            
            # Label
            color_label = ttk.Label(color_grid, text=f"{label}:")
            color_label.grid(row=row, column=col, sticky=tk.W, padx=(0, 5), pady=2)
            
            # Color button
            color_btn = tk.Button(color_grid, text="  ", width=3, height=1,
                                relief=tk.RAISED, borderwidth=2,
                                command=lambda key=color_key: self.choose_color(key))
            color_btn.grid(row=row, column=col+1, padx=(0, 15), pady=2)
            
            self.color_buttons[color_key] = color_btn
        
        # Custom theme controls
        custom_controls = tk.Frame(custom_frame)
        custom_controls.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(custom_controls, text="Save as Custom Theme", 
                  command=self.save_custom_theme).pack(side=tk.LEFT)
        
        ttk.Button(custom_controls, text="Reset to Default", 
                  command=self.reset_theme).pack(side=tk.LEFT, padx=(10, 0))
    
    def create_buttons(self, parent):
        """Create dialog buttons."""
        button_frame = tk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Buttons
        ttk.Button(button_frame, text="Apply", 
                  command=self.on_apply).pack(side=tk.RIGHT, padx=(5, 0))
        
        ttk.Button(button_frame, text="OK", 
                  command=self.on_ok).pack(side=tk.RIGHT, padx=(5, 0))
        
        ttk.Button(button_frame, text="Cancel", 
                  command=self.on_cancel).pack(side=tk.RIGHT, padx=(5, 0))
    
    def on_theme_changed(self, event=None):
        """Handle theme selection change."""
        new_theme = self.theme_var.get()
        self.theme_manager.set_theme(new_theme)
        self.update_theme_description()
        self.update_color_buttons()
        self.apply_preview_theme()
        
        if self.apply_callback:
            self.apply_callback()
    
    def update_theme_description(self):
        """Update theme description label."""
        current_theme = self.theme_var.get()
        themes = self.theme_manager.get_available_themes()
        
        if current_theme in themes:
            description = themes[current_theme]
            if self.theme_manager.is_dark_theme():
                description += " (Dark Mode)"
            self.theme_desc_label.config(text=description)
    
    def update_color_buttons(self):
        """Update color button appearances."""
        colors = self.theme_manager.get_colors()
        
        for color_key, button in self.color_buttons.items():
            color_value = colors.get(color_key, "#000000")
            button.config(bg=color_value)
            
            # Set text color for better visibility
            try:
                # Calculate brightness to determine text color
                hex_color = color_value[1:] if color_value.startswith("#") else color_value
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16) 
                b = int(hex_color[4:6], 16)
                brightness = (r * 299 + g * 587 + b * 114) / 1000
                text_color = "#000000" if brightness > 128 else "#FFFFFF"
                button.config(fg=text_color)
            except:
                button.config(fg="#000000")
    
    def choose_color(self, color_key: str):
        """Open color chooser for specific color."""
        current_color = self.theme_manager.get_color(color_key)
        
        color = colorchooser.askcolor(
            color=current_color,
            title=f"Choose {color_key.replace('_', ' ').title()}"
        )
        
        if color[1]:  # If color was selected
            # Update theme manager
            theme_id = self.theme_manager.get_current_theme()
            
            # Create custom theme if modifying built-in theme
            if theme_id in ["light", "dark", "blue"]:
                custom_theme_id = f"custom_{theme_id}"
                self.theme_manager.create_custom_theme(
                    custom_theme_id, 
                    f"Custom {theme_id.title()}", 
                    theme_id
                )
                self.theme_manager.set_theme(custom_theme_id)
                self.theme_var.set(custom_theme_id)
                
                # Update combobox values
                theme_combo = None
                for widget in self.dialog.winfo_children():
                    if isinstance(widget, ttk.Frame):
                        for child in widget.winfo_children():
                            if isinstance(child, ttk.LabelFrame):
                                for grandchild in child.winfo_children():
                                    if isinstance(grandchild, ttk.Combobox):
                                        theme_combo = grandchild
                                        break
                
                if theme_combo:
                    available_themes = self.theme_manager.get_available_themes()
                    theme_combo['values'] = list(available_themes.keys())
            
            # Update color
            self.theme_manager.update_custom_theme_color(
                self.theme_manager.get_current_theme(),
                color_key, 
                color[1]
            )
            
            # Update UI
            self.update_color_buttons()
            self.update_theme_description()
            self.apply_preview_theme()
            
            if self.apply_callback:
                self.apply_callback()
    
    def save_custom_theme(self):
        """Save current settings as custom theme."""
        # Simple name input dialog
        name = tk.simpledialog.askstring(
            "Save Custom Theme",
            "Enter theme name:",
            parent=self.dialog
        )
        
        if name:
            theme_id = f"custom_{name.lower().replace(' ', '_')}"
            
            if self.theme_manager.create_custom_theme(
                theme_id, name, self.theme_manager.get_current_theme()
            ):
                messagebox.showinfo("Success", f"Custom theme '{name}' saved!")
                
                # Update combobox
                for widget in self.dialog.winfo_children():
                    if isinstance(widget, ttk.Frame):
                        for child in widget.winfo_children():
                            if isinstance(child, ttk.LabelFrame):
                                for grandchild in child.winfo_children():
                                    if isinstance(grandchild, ttk.Combobox):
                                        available_themes = self.theme_manager.get_available_themes()
                                        grandchild['values'] = list(available_themes.keys())
                                        break
            else:
                messagebox.showerror("Error", "Failed to save custom theme.")
    
    def reset_theme(self):
        """Reset current theme to defaults."""
        current_theme = self.theme_manager.get_current_theme()
        
        if current_theme.startswith("custom_"):
            # Reset to base theme
            base_theme = current_theme.replace("custom_", "")
            if base_theme in ["light", "dark", "blue"]:
                self.theme_manager.set_theme(base_theme)
                self.theme_var.set(base_theme)
                self.update_color_buttons()
                self.update_theme_description()
                self.apply_preview_theme()
                
                if self.apply_callback:
                    self.apply_callback()
    
    def apply_current_theme(self):
        """Apply current theme to dialog."""
        themed_widget = ThemedWidget(self.theme_manager)
        
        # Apply to dialog
        try:
            self.dialog.configure(bg=self.theme_manager.get_color("bg_primary"))
        except:
            pass
        
        # Configure ttk style
        configure_ttk_style(self.theme_manager)
        
        # Update color buttons
        self.update_color_buttons()
        
        # Apply to preview
        self.apply_preview_theme()
    
    def apply_preview_theme(self):
        """Apply current theme to preview widgets."""
        if not hasattr(self, 'preview_widgets'):
            return
            
        themed_widget = ThemedWidget(self.theme_manager)
        colors = self.theme_manager.get_colors()
        
        try:
            # Apply theme to preview widgets
            themed_widget.apply_theme(self.preview_widgets['container'], "frame")
            themed_widget.apply_theme(self.preview_widgets['sample_frame'], "frame")
            themed_widget.apply_theme(self.preview_widgets['title_label'], "label")
            themed_widget.apply_theme(self.preview_widgets['subtitle_label'], "label")
            themed_widget.apply_theme(self.preview_widgets['button_frame'], "frame")
            themed_widget.apply_theme(self.preview_widgets['primary_btn'], "button_primary")
            themed_widget.apply_theme(self.preview_widgets['secondary_btn'], "button_secondary")
            themed_widget.apply_theme(self.preview_widgets['entry_frame'], "frame")
            themed_widget.apply_theme(self.preview_widgets['sample_entry'], "entry")
            themed_widget.apply_theme(self.preview_widgets['text_frame'], "frame")
            themed_widget.apply_theme(self.preview_widgets['sample_text'], "text")
            themed_widget.apply_theme(self.preview_widgets['data_frame'], "frame")
            themed_widget.apply_theme(self.preview_widgets['list_frame'], "frame")
            themed_widget.apply_theme(self.preview_widgets['sample_listbox'], "listbox")
        except Exception as e:
            print(f"Error applying preview theme: {e}")
    
    def on_apply(self):
        """Apply current theme without closing."""
        if self.apply_callback:
            self.apply_callback()
    
    def on_ok(self):
        """Accept changes and close dialog."""
        self.result = self.theme_manager.get_current_theme()
        if self.apply_callback:
            self.apply_callback()
        self.dialog.destroy()
    
    def on_cancel(self):
        """Cancel changes and close dialog."""
        # Restore original theme
        self.theme_manager.set_theme(self.original_theme)
        if self.apply_callback:
            self.apply_callback()
        self.result = None
        self.dialog.destroy()


# Import simpledialog for custom theme naming
try:
    from tkinter import simpledialog
except ImportError:
    # Fallback implementation
    class simpledialog:
        @staticmethod
        def askstring(title, prompt, parent=None):
            dialog = tk.Toplevel(parent)
            dialog.title(title)
            dialog.geometry("300x120")
            dialog.transient(parent)
            dialog.grab_set()
            
            result = [None]
            
            def on_ok():
                result[0] = entry.get()
                dialog.destroy()
            
            def on_cancel():
                dialog.destroy()
            
            # Create widgets
            tk.Label(dialog, text=prompt).pack(pady=10)
            entry = tk.Entry(dialog, width=30)
            entry.pack(pady=5)
            entry.focus()
            
            button_frame = tk.Frame(dialog)
            button_frame.pack(pady=10)
            
            tk.Button(button_frame, text="OK", command=on_ok).pack(side=tk.LEFT, padx=5)
            tk.Button(button_frame, text="Cancel", command=on_cancel).pack(side=tk.LEFT, padx=5)
            
            # Bind Enter key
            entry.bind('<Return>', lambda e: on_ok())
            
            dialog.wait_window()
            return result[0]