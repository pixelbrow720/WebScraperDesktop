"""
Scraper for Quotes to Scrape (http://quotes.toscrape.com/)
A legal demo site for scraping practice with quotes, authors, and tags.
"""

import re
from urllib.parse import urljoin

from scraper.sites.base_scraper import BaseScraper


class QuotesToScrapeScraper(BaseScraper):
    """Scraper for Quotes to Scrape website."""
    
    def get_site_info(self):
        """Get site information."""
        return {
            'name': 'Quotes to Scrape',
            'base_url': 'http://quotes.toscrape.com/',
            'description': 'Demo quotes site for scraping practice - quotes with authors and tags'
        }
        
    def get_start_url(self, category_filter=""):
        """Get starting URL, optionally filtered by tag."""
        base_url = 'http://quotes.toscrape.com/'
        
        if category_filter:
            # Quotes to Scrape uses tags - try to find matching tag
            tag_url = self.find_tag_url(category_filter)
            if tag_url:
                return tag_url
        
        return base_url
        
    def find_tag_url(self, tag_filter):
        """Find tag URL based on filter string."""
        try:
            # Get the main page to find available tags
            response = self.make_request('http://quotes.toscrape.com/')
            soup = self.parse_html(response.text)
            
            # Find tag links in sidebar
            tag_links = soup.find_all('a', class_='tag')
            for link in tag_links:
                tag_name = link.get_text(strip=True).lower()
                if tag_filter.lower() in tag_name:
                    return urljoin('http://quotes.toscrape.com/', link.get('href'))
            
        except Exception as e:
            self.logger.warning(f"Could not find tag for filter '{tag_filter}': {str(e)}")
        
        return None
        
    def get_product_links(self, page_url, max_products=None):
        """
        For quotes site, we don't have individual product pages.
        Instead, we'll extract quotes directly from listing pages.
        """
        # This scraper works differently - we extract quotes directly
        return [page_url]  # Return the page URL itself
        
    def get_next_page_url(self, current_url):
        """Get next page URL for pagination."""
        try:
            response = self.make_request(current_url)
            soup = self.parse_html(response.text)
            
            # Find next page link
            next_link = soup.find('li', class_='next')
            if next_link:
                next_a = next_link.find('a')
                if next_a:
                    return urljoin(current_url, next_a.get('href'))
            
        except Exception as e:
            self.logger.error(f"Error getting next page URL: {str(e)}")
        
        return None
        
    def scrape(self, scraper_config, progress_callback=None, stop_flag=None):
        """
        Override main scrape method for quotes site.
        Extract all quotes from listing pages instead of individual product pages.
        """
        self.logger.info("Starting quotes scraping process")
        
        max_products = scraper_config.get('max_products', 50)
        delay = scraper_config.get('delay', 1.0)
        category_filter = scraper_config.get('category_filter', '')
        
        self.scraped_data = []
        
        try:
            # Get site information
            site_info = self.get_site_info()
            self.base_url = site_info['base_url']
            
            # Get starting URL
            start_url = self.get_start_url(category_filter)
            
            if progress_callback:
                progress_callback(0, max_products, "Getting quotes...")
            
            # Scrape quotes from pages
            current_url = start_url
            page_num = 1
            
            while len(self.scraped_data) < max_products and current_url:
                if stop_flag and stop_flag():
                    break
                
                self.logger.info(f"Scraping quotes from page {page_num}: {current_url}")
                
                try:
                    quotes = self.scrape_quotes_from_page(current_url)
                    
                    for quote in quotes:
                        if len(self.scraped_data) >= max_products:
                            break
                        self.scraped_data.append(quote)
                    
                    if progress_callback:
                        progress_callback(len(self.scraped_data), max_products, 
                                        f"Scraped {len(self.scraped_data)} quotes")
                    
                    # Get next page
                    current_url = self.get_next_page_url(current_url)
                    page_num += 1
                    
                    # Rate limiting
                    if delay > 0:
                        import time
                        time.sleep(delay)
                    
                except Exception as e:
                    self.logger.error(f"Error scraping page {page_num}: {str(e)}")
                    break
            
            if progress_callback:
                progress_callback(len(self.scraped_data), max_products, "Scraping completed")
            
            # Convert to DataFrame
            import pandas as pd
            df = pd.DataFrame(self.scraped_data)
            self.logger.info(f"Scraping completed. {len(df)} quotes scraped.")
            
            return df
            
        except Exception as e:
            self.logger.error(f"Scraping failed: {str(e)}")
            raise
            
    def scrape_quotes_from_page(self, page_url):
        """Extract all quotes from a single page."""
        try:
            response = self.make_request(page_url)
            soup = self.parse_html(response.text)
            
            quotes = []
            quote_divs = soup.find_all('div', class_='quote')
            
            for quote_div in quote_divs:
                quote_data = self.extract_quote_data(quote_div, page_url)
                if quote_data:
                    quotes.append(quote_data)
            
            return quotes
            
        except Exception as e:
            self.logger.error(f"Error scraping quotes from {page_url}: {str(e)}")
            return []
            
    def extract_quote_data(self, quote_div, page_url):
        """Extract data from a single quote div."""
        try:
            # Extract quote text
            text_elem = quote_div.find('span', class_='text')
            quote_text = text_elem.get_text(strip=True) if text_elem else ""
            
            # Extract author
            author_elem = quote_div.find('small', class_='author')
            author = author_elem.get_text(strip=True) if author_elem else ""
            
            # Extract tags
            tag_elems = quote_div.find_all('a', class_='tag')
            tags = [tag.get_text(strip=True) for tag in tag_elems]
            
            # Create product-like data structure
            quote_data = {
                'name': f"Quote by {author}",  # Product name equivalent
                'price': 0.0,  # Quotes are free
                'rating': 5.0,  # All quotes are 5-star quality :)
                'url': page_url,
                'text': self.clean_text(quote_text),
                'author': self.clean_text(author),
                'tags': ', '.join(tags),
                'category': 'Quotes'
            }
            
            return quote_data
            
        except Exception as e:
            self.logger.error(f"Error extracting quote data: {str(e)}")
            return None
            
    def scrape_product(self, product_url):
        """
        Not used for quotes site since we extract directly from listing pages.
        """
        return None
        
    def is_valid_product_url(self, url):
        """Check if URL is a valid quotes URL."""
        return url and 'quotes.toscrape.com' in url
