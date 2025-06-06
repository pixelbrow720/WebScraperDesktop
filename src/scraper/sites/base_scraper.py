"""
Base scraper class that defines the interface for all site-specific scrapers.
Provides common functionality and ensures consistent behavior.
"""

import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin, urlparse
import re
from abc import ABC, abstractmethod

from utils.logger import get_logger


class BaseScraper(ABC):
    """Base class for all site-specific scrapers."""
    
    def __init__(self, session, config):
        self.session = session
        self.config = config
        self.logger = get_logger(self.__class__.__name__)
        self.base_url = None
        self.scraped_data = []
        
    @abstractmethod
    def get_site_info(self):
        """
        Get information about the site.
        
        Returns:
            dict: Site information including name, base_url, description
        """
        pass
        
    @abstractmethod
    def get_product_links(self, page_url, max_products=None):
        """
        Extract product links from a listing page.
        
        Args:
            page_url (str): URL of the listing page
            max_products (int): Maximum number of products to extract
            
        Returns:
            list: List of product URLs
        """
        pass
        
    @abstractmethod
    def scrape_product(self, product_url):
        """
        Scrape data from a single product page.
        
        Args:
            product_url (str): URL of the product page
            
        Returns:
            dict: Product data with keys: name, price, rating, url, etc.
        """
        pass
        
    def scrape(self, scraper_config, progress_callback=None, stop_flag=None):
        """
        Main scraping method that orchestrates the entire process.
        
        Args:
            scraper_config (dict): Scraping configuration
            progress_callback (callable): Progress update callback
            stop_flag (callable): Function that returns True if scraping should stop
            
        Returns:
            pandas.DataFrame: Scraped data
        """
        self.logger.info("Starting scraping process")
        
        max_products = scraper_config.get('max_products', 50)
        delay = scraper_config.get('delay', 1.0)
        category_filter = scraper_config.get('category_filter', '')
        
        self.scraped_data = []
        
        try:
            # Get site information
            site_info = self.get_site_info()
            self.base_url = site_info['base_url']
            
            # Get starting URL (could be category-specific)
            start_url = self.get_start_url(category_filter)
            
            # Get product links
            if progress_callback:
                progress_callback(0, max_products, "Getting product links...")
            
            product_links = self.get_all_product_links(start_url, max_products, stop_flag)
            
            if not product_links:
                self.logger.warning("No product links found")
                return pd.DataFrame()
            
            self.logger.info(f"Found {len(product_links)} product links")
            
            # Scrape each product
            for i, product_url in enumerate(product_links):
                if stop_flag and stop_flag():
                    self.logger.info("Scraping stopped by user")
                    break
                
                try:
                    if progress_callback:
                        progress_callback(i, len(product_links), f"Scraping product {i+1}/{len(product_links)}")
                    
                    product_data = self.scrape_product(product_url)
                    if product_data:
                        self.scraped_data.append(product_data)
                        self.logger.debug(f"Scraped product: {product_data.get('name', 'Unknown')}")
                    
                    # Rate limiting
                    if delay > 0:
                        time.sleep(delay)
                        
                except Exception as e:
                    self.logger.error(f"Error scraping product {product_url}: {str(e)}")
                    continue
            
            if progress_callback:
                progress_callback(len(product_links), len(product_links), "Scraping completed")
            
            # Convert to DataFrame
            df = pd.DataFrame(self.scraped_data)
            self.logger.info(f"Scraping completed. {len(df)} products scraped.")
            
            return df
            
        except Exception as e:
            self.logger.error(f"Scraping failed: {str(e)}")
            raise
            
    def get_start_url(self, category_filter=""):
        """
        Get the starting URL for scraping, potentially filtered by category.
        
        Args:
            category_filter (str): Category filter string
            
        Returns:
            str: Starting URL
        """
        # Default implementation returns base URL
        return self.base_url
        
    def get_all_product_links(self, start_url, max_products, stop_flag=None):
        """
        Get all product links from multiple pages if necessary.
        
        Args:
            start_url (str): Starting URL
            max_products (int): Maximum number of products
            stop_flag (callable): Stop flag function
            
        Returns:
            list: List of product URLs
        """
        all_links = []
        current_url = start_url
        page_num = 1
        
        while len(all_links) < max_products and current_url:
            if stop_flag and stop_flag():
                break
                
            self.logger.info(f"Getting links from page {page_num}: {current_url}")
            
            try:
                page_links = self.get_product_links(current_url, max_products - len(all_links))
                if not page_links:
                    break
                    
                all_links.extend(page_links)
                self.logger.info(f"Got {len(page_links)} links from page {page_num}")
                
                # Try to get next page URL
                current_url = self.get_next_page_url(current_url)
                page_num += 1
                
                # Rate limiting between pages
                time.sleep(1)
                
            except Exception as e:
                self.logger.error(f"Error getting links from page {page_num}: {str(e)}")
                break
        
        return all_links[:max_products]
        
    def get_next_page_url(self, current_url):
        """
        Get the URL of the next page for pagination.
        
        Args:
            current_url (str): Current page URL
            
        Returns:
            str: Next page URL or None if no next page
        """
        # Default implementation - subclasses should override
        return None
        
    def make_request(self, url, **kwargs):
        """
        Make HTTP request with error handling and logging.
        
        Args:
            url (str): URL to request
            **kwargs: Additional arguments for requests
            
        Returns:
            requests.Response: Response object
        """
        try:
            self.logger.debug(f"Making request to: {url}")
            response = self.session.get(url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed for {url}: {str(e)}")
            raise
            
    def parse_html(self, html_content):
        """
        Parse HTML content using BeautifulSoup.
        
        Args:
            html_content (str): HTML content
            
        Returns:
            BeautifulSoup: Parsed HTML
        """
        return BeautifulSoup(html_content, 'html.parser')
        
    def clean_text(self, text):
        """
        Clean and normalize text content.
        
        Args:
            text (str): Raw text
            
        Returns:
            str: Cleaned text
        """
        if not text:
            return ""
        
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters that might cause CSV issues
        text = re.sub(r'[^\w\s\-\.,!?()$€£¥]', '', text)
        
        return text
        
    def parse_price(self, price_text):
        """
        Parse price from text, handling various formats and currencies.
        
        Args:
            price_text (str): Raw price text
            
        Returns:
            float: Parsed price or None if parsing fails
        """
        if not price_text:
            return None
        
        # Remove currency symbols and extract numeric value
        price_text = str(price_text).strip()
        
        # Common price patterns
        price_patterns = [
            r'[\$£€¥]\s*([\d,]+\.?\d*)',  # $12.99, £10.50, etc.
            r'([\d,]+\.?\d*)\s*[\$£€¥]',  # 12.99$, 10.50£, etc.
            r'([\d,]+\.?\d*)',             # 12.99, 10.50, etc.
        ]
        
        for pattern in price_patterns:
            match = re.search(pattern, price_text)
            if match:
                try:
                    # Remove commas and convert to float
                    price_str = match.group(1).replace(',', '')
                    return float(price_str)
                except ValueError:
                    continue
        
        return None
        
    def parse_rating(self, rating_text):
        """
        Parse rating from text, handling various formats.
        
        Args:
            rating_text (str): Raw rating text
            
        Returns:
            float: Parsed rating or None if parsing fails
        """
        if not rating_text:
            return None
        
        rating_text = str(rating_text).strip()
        
        # Common rating patterns
        rating_patterns = [
            r'([\d.]+)\s*out\s*of\s*[\d.]+',  # 4.5 out of 5
            r'([\d.]+)\s*/\s*[\d.]+',         # 4.5/5
            r'([\d.]+)\s*stars?',             # 4.5 stars
            r'Rating:\s*([\d.]+)',            # Rating: 4.5
            r'([\d.]+)',                      # 4.5
        ]
        
        for pattern in rating_patterns:
            match = re.search(pattern, rating_text, re.IGNORECASE)
            if match:
                try:
                    rating = float(match.group(1))
                    # Normalize to 5-star scale if necessary
                    if rating > 5:
                        rating = rating / 2  # Assume 10-star scale
                    return min(rating, 5.0)  # Cap at 5
                except ValueError:
                    continue
        
        return None
        
    def make_absolute_url(self, url):
        """
        Convert relative URL to absolute URL.
        
        Args:
            url (str): Relative or absolute URL
            
        Returns:
            str: Absolute URL
        """
        if not url:
            return url
        
        return urljoin(self.base_url, url)
        
    def is_valid_product_url(self, url):
        """
        Check if URL is a valid product URL for this site.
        
        Args:
            url (str): URL to check
            
        Returns:
            bool: True if valid product URL
        """
        # Default implementation - subclasses should override
        return url and url.startswith(('http://', 'https://'))
        
    def extract_product_id(self, url):
        """
        Extract product ID from URL.
        
        Args:
            url (str): Product URL
            
        Returns:
            str: Product ID or None
        """
        # Default implementation - subclasses should override
        return None
