"""
Configuration management for E-Commerce Data Scraper.
Handles application settings, site configurations, and user preferences.
"""

import yaml
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
import copy

from utils.logger import get_logger


class Config:
    """Main configuration manager for the application."""
    
    def __init__(self, config_dir='config'):
        self.config_dir = Path(config_dir)
        self.logger = get_logger(__name__)
        
        # Default settings
        self.default_settings = {
            'general': {
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'timeout': 30,
                'retry_attempts': 3,
                'log_level': 'INFO'
            },
            'scraping': {
                'default_delay': 1.0,
                'max_products': 100,
                'requests_per_minute': 30,
                'skip_errors': True,
                'filter_duplicates': True
            },
            'export': {
                'default_format': 'csv',
                'csv_delimiter': ',',
                'include_headers': True,
                'date_format': '%Y-%m-%d %H:%M:%S'
            },
            'ui': {
                'window_width': 1200,
                'window_height': 800,
                'theme': 'default',
                'auto_save': True
            }
        }
        
        self.settings = {}
        self.sites_config = {}
        
        self.load_configuration()
        
    def load_configuration(self):
        """Load configuration from files."""
        try:
            # Create config directory if it doesn't exist
            self.config_dir.mkdir(exist_ok=True)
            
            # Load main settings
            self.load_settings()
            
            # Load sites configuration
            self.load_sites_config()
            
            self.logger.info("Configuration loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {str(e)}")
            # Use default settings if loading fails
            self.settings = copy.deepcopy(self.default_settings)
            
    def load_settings(self):
        """Load main application settings."""
        settings_file = self.config_dir / 'settings.yaml'
        
        try:
            if settings_file.exists():
                with open(settings_file, 'r', encoding='utf-8') as f:
                    loaded_settings = yaml.safe_load(f) or {}
                
                # Merge with defaults
                self.settings = self._merge_settings(self.default_settings, loaded_settings)
                self.logger.info(f"Settings loaded from {settings_file}")
            else:
                # Use defaults and create file
                self.settings = copy.deepcopy(self.default_settings)
                self.save_settings()
                self.logger.info("Created default settings file")
                
        except Exception as e:
            self.logger.error(f"Error loading settings: {str(e)}")
            self.settings = copy.deepcopy(self.default_settings)
            
    def load_sites_config(self):
        """Load sites configuration."""
        sites_file = self.config_dir / 'sites.yaml'
        
        try:
            if sites_file.exists():
                with open(sites_file, 'r', encoding='utf-8') as f:
                    self.sites_config = yaml.safe_load(f) or {}
                self.logger.info(f"Sites configuration loaded from {sites_file}")
            else:
                # Create default sites config
                self.sites_config = self._get_default_sites_config()
                self.save_sites_config()
                self.logger.info("Created default sites configuration")
                
        except Exception as e:
            self.logger.error(f"Error loading sites config: {str(e)}")
            self.sites_config = self._get_default_sites_config()
            
    def _merge_settings(self, default, loaded):
        """Recursively merge loaded settings with defaults."""
        result = copy.deepcopy(default)
        
        for key, value in loaded.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_settings(result[key], value)
            else:
                result[key] = value
                
        return result
        
    def _get_default_sites_config(self):
        """Get default sites configuration."""
        return {
            'Books to Scrape': {
                'base_url': 'http://books.toscrape.com/',
                'description': 'Demo bookstore for scraping practice - 1000 books with ratings and prices',
                'legal_status': 'Legal - Demo site designed for scraping',
                'rate_limit': 1.0,
                'max_pages': 50,
                'supported_categories': [
                    'Travel', 'Mystery', 'Historical Fiction', 'Sequential Art',
                    'Classics', 'Philosophy', 'Romance', 'Womens Fiction',
                    'Fiction', 'Childrens', 'Religion', 'Nonfiction',
                    'Music', 'Default', 'Science Fiction', 'Sports and Games',
                    'Add a comment', 'Fantasy', 'New Adult', 'Young Adult',
                    'Science', 'Poetry', 'Paranormal', 'Art', 'Psychology',
                    'Autobiography', 'Parenting', 'Adult Fiction', 'Humor',
                    'Horror', 'History', 'Food and Drink', 'Christian Fiction',
                    'Business', 'Biography', 'Thriller', 'Contemporary',
                    'Spirituality', 'Academic', 'Self Help', 'Historical',
                    'Christian', 'Suspense', 'Short Stories', 'Novels',
                    'Health', 'Politics', 'Cultural', 'Erotica', 'Crime'
                ]
            },
            'Quotes to Scrape': {
                'base_url': 'http://quotes.toscrape.com/',
                'description': 'Demo quotes site for scraping practice - quotes with authors and tags',
                'legal_status': 'Legal - Demo site designed for scraping',
                'rate_limit': 1.0,
                'max_pages': 10,
                'supported_tags': [
                    'change', 'deep-thoughts', 'thinking', 'world', 'abilities',
                    'choices', 'inspirational', 'life', 'live', 'miracle',
                    'miracles', 'aliteracy', 'books', 'classic', 'humor'
                ]
            }
        }
        
    def save_settings(self):
        """Save current settings to file."""
        try:
            settings_file = self.config_dir / 'settings.yaml'
            
            with open(settings_file, 'w', encoding='utf-8') as f:
                yaml.dump(self.settings, f, default_flow_style=False, 
                         allow_unicode=True, indent=2)
            
            self.logger.info(f"Settings saved to {settings_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save settings: {str(e)}")
            return False
            
    def save_sites_config(self):
        """Save sites configuration to file."""
        try:
            sites_file = self.config_dir / 'sites.yaml'
            
            with open(sites_file, 'w', encoding='utf-8') as f:
                yaml.dump(self.sites_config, f, default_flow_style=False,
                         allow_unicode=True, indent=2)
            
            self.logger.info(f"Sites configuration saved to {sites_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save sites config: {str(e)}")
            return False
            
    # Getter methods for easy access to settings
    def get_user_agent(self):
        """Get user agent string."""
        return self.settings.get('general', {}).get('user_agent', self.default_settings['general']['user_agent'])
        
    def get_timeout(self):
        """Get request timeout."""
        return self.settings.get('general', {}).get('timeout', self.default_settings['general']['timeout'])
        
    def get_retry_attempts(self):
        """Get retry attempts."""
        return self.settings.get('general', {}).get('retry_attempts', self.default_settings['general']['retry_attempts'])
        
    def get_log_level(self):
        """Get logging level."""
        return self.settings.get('general', {}).get('log_level', self.default_settings['general']['log_level'])
        
    def get_default_delay(self):
        """Get default scraping delay."""
        return self.settings.get('scraping', {}).get('default_delay', self.default_settings['scraping']['default_delay'])
        
    def get_max_products(self):
        """Get default max products."""
        return self.settings.get('scraping', {}).get('max_products', self.default_settings['scraping']['max_products'])
        
    def get_requests_per_minute(self):
        """Get requests per minute limit."""
        return self.settings.get('scraping', {}).get('requests_per_minute', self.default_settings['scraping']['requests_per_minute'])
        
    def get_available_sites(self):
        """Get available sites for scraping."""
        return self.sites_config
        
    def get_site_info(self, site_name):
        """Get information for a specific site."""
        return self.sites_config.get(site_name, {})
        
    def update_settings(self, updates):
        """
        Update settings with new values.
        
        Args:
            updates (dict): Settings to update
        """
        try:
            # Update specific settings
            if 'user_agent' in updates:
                self.settings.setdefault('general', {})['user_agent'] = updates['user_agent']
            
            if 'log_level' in updates:
                self.settings.setdefault('general', {})['log_level'] = updates['log_level']
                
            if 'timeout' in updates:
                self.settings.setdefault('general', {})['timeout'] = updates['timeout']
                
            if 'retry_attempts' in updates:
                self.settings.setdefault('general', {})['retry_attempts'] = updates['retry_attempts']
            
            # Save updated settings
            self.save_settings()
            self.logger.info("Settings updated successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to update settings: {str(e)}")
            
    def update_advanced_settings(self, advanced_settings):
        """
        Update advanced settings from settings dialog.
        
        Args:
            advanced_settings (dict): Advanced settings to update
        """
        try:
            # Network settings
            if 'accept_language' in advanced_settings:
                self.settings.setdefault('network', {})['accept_language'] = advanced_settings['accept_language']
                
            if 'accept_encoding' in advanced_settings:
                self.settings.setdefault('network', {})['accept_encoding'] = advanced_settings['accept_encoding']
                
            if 'use_proxy' in advanced_settings:
                self.settings.setdefault('network', {})['use_proxy'] = advanced_settings['use_proxy']
                
            if 'proxy_url' in advanced_settings:
                self.settings.setdefault('network', {})['proxy_url'] = advanced_settings['proxy_url']
            
            # Scraping settings
            if 'requests_per_minute' in advanced_settings:
                self.settings.setdefault('scraping', {})['requests_per_minute'] = advanced_settings['requests_per_minute']
                
            if 'min_delay' in advanced_settings:
                self.settings.setdefault('scraping', {})['min_delay'] = advanced_settings['min_delay']
                
            if 'max_delay' in advanced_settings:
                self.settings.setdefault('scraping', {})['max_delay'] = advanced_settings['max_delay']
                
            if 'skip_errors' in advanced_settings:
                self.settings.setdefault('scraping', {})['skip_errors'] = advanced_settings['skip_errors']
                
            if 'log_errors' in advanced_settings:
                self.settings.setdefault('scraping', {})['log_errors'] = advanced_settings['log_errors']
            
            # Export settings
            if 'csv_delimiter' in advanced_settings:
                self.settings.setdefault('export', {})['csv_delimiter'] = advanced_settings['csv_delimiter']
                
            if 'include_headers' in advanced_settings:
                self.settings.setdefault('export', {})['include_headers'] = advanced_settings['include_headers']
                
            if 'date_format' in advanced_settings:
                self.settings.setdefault('export', {})['date_format'] = advanced_settings['date_format']
            
            # Save updated settings
            self.save_settings()
            self.logger.info("Advanced settings updated successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to update advanced settings: {str(e)}")
            
    def reset_to_defaults(self):
        """Reset all settings to defaults."""
        try:
            self.settings = copy.deepcopy(self.default_settings)
            self.save_settings()
            self.logger.info("Settings reset to defaults")
            
        except Exception as e:
            self.logger.error(f"Failed to reset settings: {str(e)}")
            
    def get_setting(self, section, key, default=None):
        """
        Get a specific setting value.
        
        Args:
            section (str): Settings section
            key (str): Setting key
            default: Default value if setting not found
            
        Returns:
            Setting value or default
        """
        return self.settings.get(section, {}).get(key, default)
        
    def set_setting(self, section, key, value):
        """
        Set a specific setting value.
        
        Args:
            section (str): Settings section
            key (str): Setting key
            value: Setting value
        """
        self.settings.setdefault(section, {})[key] = value
        
    def export_config(self, filepath):
        """
        Export current configuration to file.
        
        Args:
            filepath (str): Export file path
            
        Returns:
            bool: True if export successful
        """
        try:
            config_data = {
                'settings': self.settings,
                'sites': self.sites_config,
                'export_date': str(Path().cwd()),
                'version': '1.0'
            }
            
            if filepath.endswith('.json'):
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(config_data, f, indent=2, ensure_ascii=False)
            else:
                with open(filepath, 'w', encoding='utf-8') as f:
                    yaml.dump(config_data, f, default_flow_style=False,
                             allow_unicode=True, indent=2)
            
            self.logger.info(f"Configuration exported to {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to export configuration: {str(e)}")
            return False
            
    def import_config(self, filepath):
        """
        Import configuration from file.
        
        Args:
            filepath (str): Import file path
            
        Returns:
            bool: True if import successful
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                if filepath.endswith('.json'):
                    config_data = json.load(f)
                else:
                    config_data = yaml.safe_load(f)
            
            # Validate and import settings
            if 'settings' in config_data:
                self.settings = self._merge_settings(self.default_settings, config_data['settings'])
                
            if 'sites' in config_data:
                self.sites_config.update(config_data['sites'])
            
            # Save imported configuration
            self.save_settings()
            self.save_sites_config()
            
            self.logger.info(f"Configuration imported from {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to import configuration: {str(e)}")
            return False
            
    def validate_config(self):
        """
        Validate current configuration.
        
        Returns:
            tuple: (is_valid, error_messages)
        """
        errors = []
        
        try:
            # Validate general settings
            if self.get_timeout() <= 0:
                errors.append("Timeout must be greater than 0")
                
            if self.get_retry_attempts() < 0:
                errors.append("Retry attempts cannot be negative")
                
            # Validate scraping settings
            if self.get_default_delay() < 0:
                errors.append("Scraping delay cannot be negative")
                
            if self.get_requests_per_minute() <= 0:
                errors.append("Requests per minute must be greater than 0")
            
            # Validate sites configuration
            for site_name, site_config in self.sites_config.items():
                if 'base_url' not in site_config:
                    errors.append(f"Site '{site_name}' missing base_url")
                    
                if not site_config.get('base_url', '').startswith(('http://', 'https://')):
                    errors.append(f"Site '{site_name}' has invalid base_url")
            
            return len(errors) == 0, errors
            
        except Exception as e:
            return False, [f"Configuration validation error: {str(e)}"]
