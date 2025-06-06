"""
Data processor for cleaning, validating, and transforming scraped data.
Ensures data quality and consistency across different data sources.
"""

import pandas as pd
import numpy as np
import re
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

from utils.logger import get_logger


class DataProcessor:
    """Process and clean scraped data for analysis and export."""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        
    def process_data(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        """
        Process raw scraped data through cleaning and validation pipeline.
        
        Args:
            raw_data (pd.DataFrame): Raw scraped data
            
        Returns:
            pd.DataFrame: Processed and cleaned data
        """
        if raw_data.empty:
            self.logger.warning("Empty dataset provided for processing")
            return raw_data
            
        self.logger.info(f"Processing {len(raw_data)} records")
        
        # Create a copy to avoid modifying original data
        processed_data = raw_data.copy()
        
        # Apply processing steps
        processed_data = self.clean_text_fields(processed_data)
        processed_data = self.standardize_prices(processed_data)
        processed_data = self.standardize_ratings(processed_data)
        processed_data = self.validate_urls(processed_data)
        processed_data = self.remove_duplicates(processed_data)
        processed_data = self.add_derived_fields(processed_data)
        processed_data = self.handle_missing_values(processed_data)
        
        self.logger.info(f"Processing completed. {len(processed_data)} records remain after cleaning")
        
        return processed_data
        
    def clean_text_fields(self, data: pd.DataFrame) -> pd.DataFrame:
        """Clean text fields by removing extra whitespace and normalizing."""
        text_columns = ['name', 'description', 'category', 'author', 'text']
        
        for col in text_columns:
            if col in data.columns:
                data[col] = data[col].astype(str).apply(self._clean_text)
                
        return data
        
    def _clean_text(self, text: str) -> str:
        """Clean individual text string."""
        if pd.isna(text) or text == 'nan':
            return ""
            
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove control characters
        text = re.sub(r'[\x00-\x1F\x7F]', '', text)
        
        # Normalize quotes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        
        return text
        
    def standardize_prices(self, data: pd.DataFrame) -> pd.DataFrame:
        """Standardize price format and handle various currencies."""
        if 'price' not in data.columns:
            return data
            
        # Convert prices to numeric format
        data['price_numeric'] = data['price'].apply(self._parse_price)
        data['currency'] = data['price'].apply(self._extract_currency)
        
        # Keep original price as string for display
        data['price_original'] = data['price'].astype(str)
        
        # Use numeric price as main price field
        data['price'] = data['price_numeric']
        
        return data
        
    def _parse_price(self, price_text: Any) -> Optional[float]:
        """Parse price from various text formats."""
        if pd.isna(price_text):
            return None
            
        price_str = str(price_text).strip()
        
        # Handle zero or free items
        if price_str.lower() in ['free', '0', '0.00', '']:
            return 0.0
            
        # Extract numeric value using regex
        price_patterns = [
            r'[\$£€¥₹]\s*([\d,]+\.?\d*)',  # Currency symbol before
            r'([\d,]+\.?\d*)\s*[\$£€¥₹]',  # Currency symbol after  
            r'([\d,]+\.?\d*)',             # Just numbers
        ]
        
        for pattern in price_patterns:
            match = re.search(pattern, price_str)
            if match:
                try:
                    # Remove commas and convert to float
                    clean_price = match.group(1).replace(',', '')
                    return float(clean_price)
                except ValueError:
                    continue
                    
        return None
        
    def _extract_currency(self, price_text: Any) -> str:
        """Extract currency symbol from price text."""
        if pd.isna(price_text):
            return "USD"  # Default currency
            
        price_str = str(price_text)
        
        currency_symbols = {
            '$': 'USD',
            '£': 'GBP', 
            '€': 'EUR',
            '¥': 'JPY',
            '₹': 'INR'
        }
        
        for symbol, currency in currency_symbols.items():
            if symbol in price_str:
                return currency
                
        return "USD"  # Default
        
    def standardize_ratings(self, data: pd.DataFrame) -> pd.DataFrame:
        """Standardize rating values to consistent scale."""
        if 'rating' not in data.columns:
            return data
            
        data['rating_numeric'] = data['rating'].apply(self._parse_rating)
        data['rating_original'] = data['rating'].astype(str)
        data['rating'] = data['rating_numeric']
        
        return data
        
    def _parse_rating(self, rating_text: Any) -> Optional[float]:
        """Parse rating from various text formats."""
        if pd.isna(rating_text):
            return None
            
        rating_str = str(rating_text).strip()
        
        # Extract numeric rating
        rating_patterns = [
            r'([\d.]+)\s*out\s*of\s*[\d.]+',  # 4.5 out of 5
            r'([\d.]+)\s*/\s*[\d.]+',         # 4.5/5
            r'([\d.]+)\s*stars?',             # 4.5 stars
            r'Rating:\s*([\d.]+)',            # Rating: 4.5
            r'([\d.]+)',                      # 4.5
        ]
        
        for pattern in rating_patterns:
            match = re.search(pattern, rating_str, re.IGNORECASE)
            if match:
                try:
                    rating = float(match.group(1))
                    # Normalize to 5-star scale
                    if rating > 10:
                        rating = rating / 20  # 100-point scale
                    elif rating > 5:
                        rating = rating / 2   # 10-point scale
                    return min(max(rating, 0), 5)  # Clamp between 0 and 5
                except ValueError:
                    continue
                    
        return None
        
    def validate_urls(self, data: pd.DataFrame) -> pd.DataFrame:
        """Validate and clean URL fields."""
        if 'url' not in data.columns:
            return data
            
        data['url_valid'] = data['url'].apply(self._is_valid_url)
        
        # Log invalid URLs
        invalid_urls = data[~data['url_valid']]['url'].tolist()
        if invalid_urls:
            self.logger.warning(f"Found {len(invalid_urls)} invalid URLs")
            
        return data
        
    def _is_valid_url(self, url: Any) -> bool:
        """Check if URL is valid."""
        if pd.isna(url):
            return False
            
        url_str = str(url).strip()
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        return bool(url_pattern.match(url_str))
        
    def remove_duplicates(self, data: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicate records based on multiple criteria."""
        initial_count = len(data)
        
        # Remove exact duplicates
        data = data.drop_duplicates()
        
        # Remove duplicates based on name and URL if available
        if 'name' in data.columns and 'url' in data.columns:
            data = data.drop_duplicates(subset=['name', 'url'], keep='first')
        elif 'name' in data.columns:
            data = data.drop_duplicates(subset=['name'], keep='first')
            
        duplicates_removed = initial_count - len(data)
        if duplicates_removed > 0:
            self.logger.info(f"Removed {duplicates_removed} duplicate records")
            
        return data
        
    def add_derived_fields(self, data: pd.DataFrame) -> pd.DataFrame:
        """Add derived/calculated fields to the dataset."""
        # Add processing timestamp
        data['processed_at'] = datetime.now().isoformat()
        
        # Add price categories if price data exists
        if 'price' in data.columns and data['price'].notna().any():
            data['price_category'] = data['price'].apply(self._categorize_price)
            
        # Add rating categories if rating data exists
        if 'rating' in data.columns and data['rating'].notna().any():
            data['rating_category'] = data['rating'].apply(self._categorize_rating)
            
        # Add name length for analysis
        if 'name' in data.columns:
            data['name_length'] = data['name'].str.len()
            
        # Add word count for descriptions
        if 'description' in data.columns:
            data['description_words'] = data['description'].str.split().str.len()
            
        return data
        
    def _categorize_price(self, price: Any) -> str:
        """Categorize price into ranges."""
        if pd.isna(price) or price is None:
            return "Unknown"
            
        try:
            price_val = float(price)
            if price_val == 0:
                return "Free"
            elif price_val < 10:
                return "Budget"
            elif price_val < 50:
                return "Moderate"
            elif price_val < 100:
                return "Premium"
            else:
                return "Luxury"
        except (ValueError, TypeError):
            return "Unknown"
            
    def _categorize_rating(self, rating: Any) -> str:
        """Categorize rating into quality levels."""
        if pd.isna(rating) or rating is None:
            return "Unrated"
            
        try:
            rating_val = float(rating)
            if rating_val >= 4.5:
                return "Excellent"
            elif rating_val >= 4.0:
                return "Very Good"
            elif rating_val >= 3.0:
                return "Good"
            elif rating_val >= 2.0:
                return "Fair"
            else:
                return "Poor"
        except (ValueError, TypeError):
            return "Unrated"
            
    def handle_missing_values(self, data: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values using appropriate strategies."""
        # Fill missing categorical fields
        categorical_fills = {
            'category': 'Uncategorized',
            'currency': 'USD',
            'rating_category': 'Unrated',
            'price_category': 'Unknown'
        }
        
        for col, fill_value in categorical_fills.items():
            if col in data.columns:
                data[col] = data[col].fillna(fill_value)
                
        # Fill missing numeric fields
        numeric_fills = {
            'price': 0.0,
            'rating': None,  # Keep ratings as None if missing
            'name_length': 0,
            'description_words': 0
        }
        
        for col, fill_value in numeric_fills.items():
            if col in data.columns:
                if fill_value is not None:
                    data[col] = data[col].fillna(fill_value)
                    
        # Fill missing text fields
        text_fills = {
            'name': 'Unknown Product',
            'description': '',
            'author': 'Unknown',
            'text': ''
        }
        
        for col, fill_value in text_fills.items():
            if col in data.columns:
                data[col] = data[col].fillna(fill_value)
                
        return data
        
    def get_data_quality_report(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Generate a data quality report."""
        if data.empty:
            return {"error": "No data to analyze"}
            
        report = {
            "total_records": len(data),
            "columns": list(data.columns),
            "missing_values": {},
            "data_types": {},
            "unique_values": {},
            "value_ranges": {}
        }
        
        for col in data.columns:
            # Missing values
            missing_count = data[col].isna().sum()
            report["missing_values"][col] = {
                "count": int(missing_count),
                "percentage": float(missing_count / len(data) * 100)
            }
            
            # Data types
            report["data_types"][col] = str(data[col].dtype)
            
            # Unique values
            unique_count = data[col].nunique()
            report["unique_values"][col] = int(unique_count)
            
            # Value ranges for numeric columns
            if pd.api.types.is_numeric_dtype(data[col]):
                valid_values = data[col].dropna()
                if len(valid_values) > 0:
                    report["value_ranges"][col] = {
                        "min": float(valid_values.min()),
                        "max": float(valid_values.max()),
                        "mean": float(valid_values.mean()),
                        "median": float(valid_values.median())
                    }
                    
        return report
        
    def export_quality_report(self, data: pd.DataFrame, filepath: str) -> bool:
        """Export data quality report to file."""
        try:
            report = self.get_data_quality_report(data)
            
            import json
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
                
            self.logger.info(f"Data quality report exported to {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to export quality report: {str(e)}")
            return False
