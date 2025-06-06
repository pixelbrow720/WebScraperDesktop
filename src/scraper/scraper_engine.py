"""
Main scraper engine that orchestrates web scraping operations.
Handles rate limiting, error recovery, and data coordination.
"""

import time
import random
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pandas as pd
from urllib.parse import urljoin
import threading
from queue import Queue, Empty

from utils.logger import get_logger
from scraper.sites.books_toscrape import BooksToScrapeScraper
from scraper.sites.quotes_toscrape import QuotesToScrapeScraper


class ScraperEngine:
    """Main scraping engine that coordinates all scraping operations."""
    
    def __init__(self, config):
        self.config = config
        self.logger = get_logger(__name__)
        self.session = None
        self.stop_scraping = False
        
        # Available scrapers
        self.scrapers = {
            'Books to Scrape': BooksToScrapeScraper,
            'Quotes to Scrape': QuotesToScrapeScraper
        }
        
        self.setup_session()
        
    def setup_session(self):
        """Setup HTTP session with retry strategy and headers."""
        self.session = requests.Session()
        
        # Retry strategy
        retry_strategy = Retry(
            total=self.config.get_retry_attempts(),
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Set headers
        headers = {
            'User-Agent': self.config.get_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.session.headers.update(headers)
        
        # Set timeout
        self.session.timeout = self.config.get_timeout()
        
        self.logger.info("HTTP session configured successfully")
        
    def get_available_sites(self):
        """Get list of available sites for scraping."""
        return list(self.scrapers.keys())
        
    def scrape_site(self, site_name, scraper_config, progress_callback=None):
        """
        Scrape a specific site with given configuration.
        
        Args:
            site_name (str): Name of the site to scrape
            scraper_config (dict): Configuration for scraping
            progress_callback (callable): Progress update callback
            
        Returns:
            pandas.DataFrame: Scraped data
        """
        if site_name not in self.scrapers:
            raise ValueError(f"Unknown site: {site_name}")
        
        self.logger.info(f"Starting scraping for site: {site_name}")
        self.stop_scraping = False
        
        # Initialize scraper
        scraper_class = self.scrapers[site_name]
        scraper = scraper_class(self.session, self.config)
        
        try:
            # Get site configuration
            site_config = self.config.get_site_info(site_name)
            
            # Start scraping
            results = scraper.scrape(
                scraper_config,
                progress_callback=progress_callback,
                stop_flag=lambda: self.stop_scraping
            )
            
            self.logger.info(f"Scraping completed for {site_name}. {len(results)} items scraped.")
            return results
            
        except Exception as e:
            self.logger.error(f"Scraping failed for {site_name}: {str(e)}")
            raise
            
    def stop(self):
        """Stop the scraping process."""
        self.stop_scraping = True
        self.logger.info("Scraping stop requested")
        
    def __del__(self):
        """Cleanup resources."""
        if self.session:
            self.session.close()


class RateLimiter:
    """Rate limiter to control request frequency."""
    
    def __init__(self, min_delay=1.0, max_delay=3.0, requests_per_minute=30):
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.requests_per_minute = requests_per_minute
        self.last_request_time = 0
        self.request_times = Queue()
        self.lock = threading.Lock()
        
    def wait(self):
        """Wait before making the next request."""
        with self.lock:
            current_time = time.time()
            
            # Remove old request times (older than 1 minute)
            while not self.request_times.empty():
                try:
                    old_time = self.request_times.get_nowait()
                    if current_time - old_time < 60:
                        self.request_times.put(old_time)
                        break
                except Empty:
                    break
            
            # Check if we need to wait due to rate limiting
            if self.request_times.qsize() >= self.requests_per_minute:
                sleep_time = 60 - (current_time - self.request_times.queue[0])
                if sleep_time > 0:
                    time.sleep(sleep_time)
            
            # Random delay between requests
            delay = random.uniform(self.min_delay, self.max_delay)
            time_since_last = current_time - self.last_request_time
            
            if time_since_last < delay:
                time.sleep(delay - time_since_last)
            
            self.last_request_time = time.time()
            self.request_times.put(self.last_request_time)


class ProxyRotator:
    """Proxy rotation manager for distributed scraping."""
    
    def __init__(self, proxy_list=None):
        self.proxy_list = proxy_list or []
        self.current_proxy_index = 0
        self.failed_proxies = set()
        self.lock = threading.Lock()
        
    def get_proxy(self):
        """Get next available proxy."""
        if not self.proxy_list:
            return None
            
        with self.lock:
            for _ in range(len(self.proxy_list)):
                proxy = self.proxy_list[self.current_proxy_index]
                self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxy_list)
                
                if proxy not in self.failed_proxies:
                    return {'http': proxy, 'https': proxy}
            
            # All proxies failed, reset and try again
            self.failed_proxies.clear()
            return self.get_proxy()
    
    def mark_proxy_failed(self, proxy):
        """Mark a proxy as failed."""
        if proxy:
            with self.lock:
                proxy_url = proxy.get('http') or proxy.get('https')
                if proxy_url:
                    self.failed_proxies.add(proxy_url)


class ScrapingStats:
    """Statistics collector for scraping operations."""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.total_items_scraped = 0
        self.errors = []
        
    def start(self):
        """Start tracking statistics."""
        self.start_time = time.time()
        
    def end(self):
        """End tracking statistics."""
        self.end_time = time.time()
        
    def add_request(self, success=True, error=None):
        """Add a request to statistics."""
        self.total_requests += 1
        if success:
            self.successful_requests += 1
        else:
            self.failed_requests += 1
            if error:
                self.errors.append(str(error))
                
    def add_item(self):
        """Add a scraped item to statistics."""
        self.total_items_scraped += 1
        
    def get_summary(self):
        """Get statistics summary."""
        duration = self.end_time - self.start_time if self.end_time and self.start_time else 0
        
        return {
            'duration': duration,
            'total_requests': self.total_requests,
            'successful_requests': self.successful_requests,
            'failed_requests': self.failed_requests,
            'success_rate': (self.successful_requests / self.total_requests * 100) if self.total_requests > 0 else 0,
            'total_items_scraped': self.total_items_scraped,
            'scraping_rate': (self.total_items_scraped / duration * 60) if duration > 0 else 0,  # items per minute
            'errors': self.errors
        }
        
    def __str__(self):
        """String representation of statistics."""
        summary = self.get_summary()
        return f"""
Scraping Statistics:
Duration: {summary['duration']:.2f} seconds
Total Requests: {summary['total_requests']}
Successful: {summary['successful_requests']} ({summary['success_rate']:.1f}%)
Failed: {summary['failed_requests']}
Items Scraped: {summary['total_items_scraped']}
Scraping Rate: {summary['scraping_rate']:.1f} items/minute
"""
