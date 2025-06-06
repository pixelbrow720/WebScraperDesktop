"""
Theme management for E-Commerce Data Scraper
Handles color themes, dark mode, and visual styling configurations.
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Tuple
import json
import os


class ThemeManager:
    """Manage application themes and color schemes."""
    
    def __init__(self):
        self.current_theme = "light"
        self.themes = self._load_default_themes()
        self.custom_themes = {}
        self.load_custom_themes()
        
    def _load_default_themes(self) -> Dict[str, Dict[str, Any]]:
        """Load default theme configurations."""
        return {
            "light": {
                "name": "Light Theme",
                "colors": {
                    # Background colors
                    "bg_primary": "#FFFFFF",
                    "bg_secondary": "#F5F5F5",
                    "bg_tertiary": "#E8E8E8",
                    "bg_accent": "#E3F2FD",
                    
                    # Text colors
                    "text_primary": "#000000",
                    "text_secondary": "#333333",
                    "text_muted": "#666666",
                    "text_inverse": "#FFFFFF",
                    
                    # Button colors
                    "btn_primary": "#2196F3",
                    "btn_primary_hover": "#1976D2",
                    "btn_secondary": "#757575",
                    "btn_secondary_hover": "#616161",
                    "btn_success": "#4CAF50",
                    "btn_success_hover": "#45A049",
                    "btn_danger": "#F44336",
                    "btn_danger_hover": "#D32F2F",
                    
                    # Border colors
                    "border_light": "#E0E0E0",
                    "border_medium": "#BDBDBD",
                    "border_dark": "#9E9E9E",
                    
                    # Status colors
                    "success": "#4CAF50",
                    "warning": "#FF9800",
                    "error": "#F44336",
                    "info": "#2196F3",
                    
                    # Chart colors
                    "chart_primary": "#2196F3",
                    "chart_secondary": "#FFC107",
                    "chart_tertiary": "#4CAF50",
                    "chart_quaternary": "#FF5722",
                    
                    # Selection colors
                    "selection": "#BBDEFB",
                    "selection_dark": "#90CAF9",
                    
                    # Tab colors
                    "tab_selected": "#2196F3",
                    "tab_normal": "#F5F5F5",
                    "tab_hover": "#E3F2FD"
                }
            },
            
            "dark": {
                "name": "Dark Theme",
                "colors": {
                    # Background colors
                    "bg_primary": "#1E1E1E",
                    "bg_secondary": "#2D2D2D",
                    "bg_tertiary": "#3C3C3C",
                    "bg_accent": "#0D47A1",
                    
                    # Text colors
                    "text_primary": "#FFFFFF",
                    "text_secondary": "#E0E0E0",
                    "text_muted": "#B0B0B0",
                    "text_inverse": "#000000",
                    
                    # Button colors
                    "btn_primary": "#1976D2",
                    "btn_primary_hover": "#1565C0",
                    "btn_secondary": "#616161",
                    "btn_secondary_hover": "#757575",
                    "btn_success": "#388E3C",
                    "btn_success_hover": "#4CAF50",
                    "btn_danger": "#D32F2F",
                    "btn_danger_hover": "#F44336",
                    
                    # Border colors
                    "border_light": "#404040",
                    "border_medium": "#505050",
                    "border_dark": "#606060",
                    
                    # Status colors
                    "success": "#4CAF50",
                    "warning": "#FF9800",
                    "error": "#F44336",
                    "info": "#2196F3",
                    
                    # Chart colors
                    "chart_primary": "#42A5F5",
                    "chart_secondary": "#FFCA28",
                    "chart_tertiary": "#66BB6A",
                    "chart_quaternary": "#FF7043",
                    
                    # Selection colors
                    "selection": "#1565C0",
                    "selection_dark": "#0D47A1",
                    
                    # Tab colors
                    "tab_selected": "#1976D2",
                    "tab_normal": "#2D2D2D",
                    "tab_hover": "#0D47A1"
                }
            },
            
            "blue": {
                "name": "Blue Professional",
                "colors": {
                    # Background colors
                    "bg_primary": "#F8FAFF",
                    "bg_secondary": "#E8F2FF",
                    "bg_tertiary": "#D1E7FF",
                    "bg_accent": "#BBDEFB",
                    
                    # Text colors
                    "text_primary": "#0D47A1",
                    "text_secondary": "#1565C0",
                    "text_muted": "#1976D2",
                    "text_inverse": "#FFFFFF",
                    
                    # Button colors
                    "btn_primary": "#1976D2",
                    "btn_primary_hover": "#1565C0",
                    "btn_secondary": "#42A5F5",
                    "btn_secondary_hover": "#1E88E5",
                    "btn_success": "#4CAF50",
                    "btn_success_hover": "#45A049",
                    "btn_danger": "#F44336",
                    "btn_danger_hover": "#D32F2F",
                    
                    # Border colors
                    "border_light": "#BBDEFB",
                    "border_medium": "#90CAF9",
                    "border_dark": "#64B5F6",
                    
                    # Status colors
                    "success": "#4CAF50",
                    "warning": "#FF9800",
                    "error": "#F44336",
                    "info": "#2196F3",
                    
                    # Chart colors
                    "chart_primary": "#1976D2",
                    "chart_secondary": "#FFC107",
                    "chart_tertiary": "#4CAF50",
                    "chart_quaternary": "#FF5722",
                    
                    # Selection colors
                    "selection": "#BBDEFB",
                    "selection_dark": "#90CAF9",
                    
                    # Tab colors
                    "tab_selected": "#1976D2",
                    "tab_normal": "#E8F2FF",
                    "tab_hover": "#BBDEFB"
                }
            }
        }
    
    def get_available_themes(self) -> Dict[str, str]:
        """Get list of available themes with their display names."""
        themes = {}
        for theme_id, theme_data in self.themes.items():
            themes[theme_id] = theme_data["name"]
        for theme_id, theme_data in self.custom_themes.items():
            themes[theme_id] = theme_data["name"]
        return themes
    
    def get_current_theme(self) -> str:
        """Get current theme ID."""
        return self.current_theme
    
    def set_theme(self, theme_id: str) -> bool:
        """Set current theme."""
        if theme_id in self.themes or theme_id in self.custom_themes:
            self.current_theme = theme_id
            return True
        return False
    
    def get_color(self, color_key: str) -> str:
        """Get color value for current theme."""
        theme_data = self._get_theme_data(self.current_theme)
        if theme_data and "colors" in theme_data:
            return theme_data["colors"].get(color_key, "#000000")
        return "#000000"
    
    def get_colors(self) -> Dict[str, str]:
        """Get all colors for current theme."""
        theme_data = self._get_theme_data(self.current_theme)
        if theme_data and "colors" in theme_data:
            return theme_data["colors"]
        return {}
    
    def _get_theme_data(self, theme_id: str) -> Dict[str, Any]:
        """Get theme data by ID."""
        if theme_id in self.themes:
            return self.themes[theme_id]
        elif theme_id in self.custom_themes:
            return self.custom_themes[theme_id]
        return {}
    
    def is_dark_theme(self) -> bool:
        """Check if current theme is dark."""
        bg_color = self.get_color("bg_primary")
        # Simple check based on background brightness
        if bg_color.startswith("#"):
            try:
                # Convert hex to RGB and calculate brightness
                hex_color = bg_color[1:]
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
                brightness = (r * 299 + g * 587 + b * 114) / 1000
                return brightness < 128
            except:
                pass
        return self.current_theme == "dark"
    
    def load_custom_themes(self):
        """Load custom themes from file."""
        try:
            themes_file = os.path.join("config", "custom_themes.json")
            if os.path.exists(themes_file):
                with open(themes_file, 'r') as f:
                    self.custom_themes = json.load(f)
        except Exception as e:
            print(f"Error loading custom themes: {e}")
            self.custom_themes = {}
    
    def save_custom_themes(self):
        """Save custom themes to file."""
        try:
            os.makedirs("config", exist_ok=True)
            themes_file = os.path.join("config", "custom_themes.json")
            with open(themes_file, 'w') as f:
                json.dump(self.custom_themes, f, indent=2)
        except Exception as e:
            print(f"Error saving custom themes: {e}")
    
    def create_custom_theme(self, theme_id: str, theme_name: str, base_theme: str = "light") -> bool:
        """Create a new custom theme based on existing theme."""
        try:
            base_data = self._get_theme_data(base_theme)
            if base_data:
                self.custom_themes[theme_id] = {
                    "name": theme_name,
                    "colors": base_data["colors"].copy()
                }
                self.save_custom_themes()
                return True
        except Exception as e:
            print(f"Error creating custom theme: {e}")
        return False
    
    def update_custom_theme_color(self, theme_id: str, color_key: str, color_value: str) -> bool:
        """Update a color in custom theme."""
        try:
            if theme_id in self.custom_themes:
                self.custom_themes[theme_id]["colors"][color_key] = color_value
                self.save_custom_themes()
                return True
        except Exception as e:
            print(f"Error updating custom theme color: {e}")
        return False
    
    def delete_custom_theme(self, theme_id: str) -> bool:
        """Delete a custom theme."""
        try:
            if theme_id in self.custom_themes:
                del self.custom_themes[theme_id]
                self.save_custom_themes()
                return True
        except Exception as e:
            print(f"Error deleting custom theme: {e}")
        return False


class ThemedWidget:
    """Base class for widgets that support theming."""
    
    def __init__(self, theme_manager: ThemeManager):
        self.theme_manager = theme_manager
        
    def apply_theme(self, widget, widget_type: str = "default"):
        """Apply current theme to widget."""
        colors = self.theme_manager.get_colors()
        
        try:
            if widget_type == "frame":
                widget.configure(bg=colors.get("bg_primary"))
            elif widget_type == "frame_secondary":
                widget.configure(bg=colors.get("bg_secondary"))
            elif widget_type == "label":
                widget.configure(
                    bg=colors.get("bg_primary"),
                    fg=colors.get("text_primary")
                )
            elif widget_type == "label_secondary":
                widget.configure(
                    bg=colors.get("bg_secondary"),
                    fg=colors.get("text_secondary")
                )
            elif widget_type == "button_primary":
                widget.configure(
                    bg=colors.get("btn_primary"),
                    fg=colors.get("text_inverse"),
                    activebackground=colors.get("btn_primary_hover")
                )
            elif widget_type == "button_secondary":
                widget.configure(
                    bg=colors.get("btn_secondary"),
                    fg=colors.get("text_inverse"),
                    activebackground=colors.get("btn_secondary_hover")
                )
            elif widget_type == "entry":
                widget.configure(
                    bg=colors.get("bg_primary"),
                    fg=colors.get("text_primary"),
                    insertbackground=colors.get("text_primary"),
                    selectbackground=colors.get("selection")
                )
            elif widget_type == "text":
                widget.configure(
                    bg=colors.get("bg_primary"),
                    fg=colors.get("text_primary"),
                    insertbackground=colors.get("text_primary"),
                    selectbackground=colors.get("selection")
                )
            elif widget_type == "listbox":
                widget.configure(
                    bg=colors.get("bg_primary"),
                    fg=colors.get("text_primary"),
                    selectbackground=colors.get("selection"),
                    selectforeground=colors.get("text_primary")
                )
        except Exception as e:
            print(f"Error applying theme to widget: {e}")


def configure_ttk_style(theme_manager: ThemeManager):
    """Configure ttk style based on current theme."""
    colors = theme_manager.get_colors()
    style = ttk.Style()
    
    try:
        # Configure Notebook (tabs)
        style.configure("TNotebook", 
                       background=colors.get("bg_primary"),
                       borderwidth=0)
        
        style.configure("TNotebook.Tab",
                       background=colors.get("tab_normal"),
                       foreground=colors.get("text_primary"),
                       padding=[12, 8],
                       borderwidth=1)
        
        style.map("TNotebook.Tab",
                 background=[("selected", colors.get("tab_selected")),
                           ("active", colors.get("tab_hover"))],
                 foreground=[("selected", colors.get("text_inverse")),
                           ("active", colors.get("text_primary"))])
        
        # Configure Frame
        style.configure("TFrame",
                       background=colors.get("bg_primary"))
        
        # Configure Label
        style.configure("TLabel",
                       background=colors.get("bg_primary"),
                       foreground=colors.get("text_primary"))
        
        # Configure Button
        style.configure("TButton",
                       background=colors.get("btn_secondary"),
                       foreground=colors.get("text_inverse"),
                       borderwidth=1,
                       focuscolor="none")
        
        style.map("TButton",
                 background=[("active", colors.get("btn_secondary_hover"))])
        
        # Configure Entry
        style.configure("TEntry",
                       fieldbackground=colors.get("bg_primary"),
                       foreground=colors.get("text_primary"),
                       borderwidth=1,
                       insertcolor=colors.get("text_primary"))
        
        # Configure Combobox
        style.configure("TCombobox",
                       fieldbackground=colors.get("bg_primary"),
                       foreground=colors.get("text_primary"),
                       borderwidth=1)
        
        # Configure Scale
        style.configure("TScale",
                       background=colors.get("bg_primary"),
                       troughcolor=colors.get("bg_tertiary"),
                       borderwidth=1)
        
        # Configure Progressbar
        style.configure("TProgressbar",
                       background=colors.get("btn_primary"),
                       troughcolor=colors.get("bg_tertiary"),
                       borderwidth=1)
        
        # Configure Checkbutton
        style.configure("TCheckbutton",
                       background=colors.get("bg_primary"),
                       foreground=colors.get("text_primary"),
                       focuscolor="none")
        
        # Configure Radiobutton  
        style.configure("TRadiobutton",
                       background=colors.get("bg_primary"),
                       foreground=colors.get("text_primary"),
                       focuscolor="none")
        
    except Exception as e:
        print(f"Error configuring ttk style: {e}")


def get_matplotlib_style(theme_manager: ThemeManager) -> Dict[str, Any]:
    """Get matplotlib style configuration for current theme."""
    colors = theme_manager.get_colors()
    is_dark = theme_manager.is_dark_theme()
    
    style_config = {
        'figure.facecolor': colors.get("bg_primary"),
        'axes.facecolor': colors.get("bg_primary"),
        'axes.edgecolor': colors.get("border_medium"),
        'axes.labelcolor': colors.get("text_primary"),
        'axes.axisbelow': True,
        'axes.grid': True,
        'axes.spines.left': True,
        'axes.spines.bottom': True,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'grid.color': colors.get("border_light"),
        'grid.alpha': 0.7,
        'text.color': colors.get("text_primary"),
        'xtick.color': colors.get("text_secondary"),
        'ytick.color': colors.get("text_secondary"),
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.facecolor': colors.get("bg_secondary"),
        'legend.edgecolor': colors.get("border_medium"),
        'legend.fontsize': 10
    }
    
    return style_config


def get_chart_colors(theme_manager: ThemeManager) -> list:
    """Get color palette for charts."""
    colors = theme_manager.get_colors()
    return [
        colors.get("chart_primary"),
        colors.get("chart_secondary"),
        colors.get("chart_tertiary"),
        colors.get("chart_quaternary"),
        colors.get("btn_primary"),
        colors.get("success"),
        colors.get("warning"),
        colors.get("error")
    ]