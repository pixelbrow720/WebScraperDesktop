"""
Scraper for Books to Scrape (http://books.toscrape.com/)
A legal demo e-commerce site designed for scraping practice.
"""

import re
from urllib.parse import urljoin

from scraper.sites.base_scraper import BaseScraper


class BooksToScrapeScraper(BaseScraper):
    """Scraper for Books to Scrape website."""
    
    def get_site_info(self):
        """Get site information."""
        return {
            'name': 'Books to Scrape',
            'base_url': 'http://books.toscrape.com/',
            'description': 'Demo bookstore for scraping practice - 1000 books with ratings and prices'
        }
        
    def get_start_url(self, category_filter=""):
        """Get starting URL, optionally filtered by category."""
        base_url = 'http://books.toscrape.com/'
        
        if category_filter:
            # Books to Scrape has category pages - try to match the filter
            category_url = self.find_category_url(category_filter)
            if category_url:
                return category_url
        
        return base_url
        
    def find_category_url(self, category_filter):
        """Find category URL based on filter string."""
        try:
            # Get the main page to find categories
            response = self.make_request('http://books.toscrape.com/')
            soup = self.parse_html(response.text)
            
            # Find category links in sidebar
            sidebar = soup.find('div', class_='side_categories')
            if sidebar:
                category_links = sidebar.find_all('a')
                for link in category_links:
                    category_name = link.get_text(strip=True).lower()
                    if category_filter.lower() in category_name:
                        return urljoin('http://books.toscrape.com/', link.get('href'))
            
        except Exception as e:
            self.logger.warning(f"Could not find category for filter '{category_filter}': {str(e)}")
        
        return None
        
    def get_product_links(self, page_url, max_products=None):
        """Extract book links from a catalog page."""
        try:
            response = self.make_request(page_url)
            soup = self.parse_html(response.text)
            
            # Find all book articles
            book_articles = soup.find_all('article', class_='product_pod')
            
            links = []
            for article in book_articles:
                if max_products and len(links) >= max_products:
                    break
                    
                # Find the book link
                title_link = article.find('h3').find('a')
                if title_link:
                    book_url = urljoin(page_url, title_link.get('href'))
                    links.append(book_url)
            
            self.logger.info(f"Found {len(links)} book links on page")
            return links
            
        except Exception as e:
            self.logger.error(f"Error getting product links from {page_url}: {str(e)}")
            return []
            
    def get_next_page_url(self, current_url):
        """Get next page URL for pagination."""
        try:
            response = self.make_request(current_url)
            soup = self.parse_html(response.text)
            
            # Find next page link
            pager = soup.find('li', class_='next')
            if pager:
                next_link = pager.find('a')
                if next_link:
                    return urljoin(current_url, next_link.get('href'))
            
        except Exception as e:
            self.logger.error(f"Error getting next page URL: {str(e)}")
        
        return None
        
    def scrape_product(self, product_url):
        """Scrape data from a single book page."""
        try:
            response = self.make_request(product_url)
            soup = self.parse_html(response.text)
            
            # Extract book data
            product_data = {
                'url': product_url,
                'name': self.extract_title(soup),
                'price': self.extract_price(soup),
                'rating': self.extract_rating(soup),
                'availability': self.extract_availability(soup),
                'description': self.extract_description(soup),
                'category': self.extract_category(soup),
                'upc': self.extract_upc(soup)
            }
            
            # Clean the data
            for key, value in product_data.items():
                if isinstance(value, str):
                    product_data[key] = self.clean_text(value)
            
            return product_data
            
        except Exception as e:
            self.logger.error(f"Error scraping product {product_url}: {str(e)}")
            return None
            
    def extract_title(self, soup):
        """Extract book title."""
        title_elem = soup.find('h1')
        return title_elem.get_text(strip=True) if title_elem else "Unknown Title"
        
    def extract_price(self, soup):
        """Extract book price."""
        price_elem = soup.find('p', class_='price_color')
        if price_elem:
            price_text = price_elem.get_text(strip=True)
            return self.parse_price(price_text)
        return None
        
    def extract_rating(self, soup):
        """Extract book rating."""
        rating_elem = soup.find('p', class_=re.compile(r'star-rating'))
        if rating_elem:
            # Extract rating from class name (e.g., "star-rating Three" -> 3)
            rating_classes = rating_elem.get('class', [])
            rating_words = {
                'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5
            }
            
            for class_name in rating_classes:
                if class_name in rating_words:
                    return float(rating_words[class_name])
        
        return None
        
    def extract_availability(self, soup):
        """Extract availability information."""
        availability_elem = soup.find('p', class_='instock availability')
        if availability_elem:
            text = availability_elem.get_text(strip=True)
            # Extract number from text like "In stock (22 available)"
            match = re.search(r'\((\d+) available\)', text)
            if match:
                return int(match.group(1))
            elif 'in stock' in text.lower():
                return 1  # Available but quantity not specified
        
        return 0
        
    def extract_description(self, soup):
        """Extract book description."""
        # Look for description in product description section
        desc_section = soup.find('div', id='product_description')
        if desc_section:
            desc_elem = desc_section.find_next_sibling('p')
            if desc_elem:
                return desc_elem.get_text(strip=True)
        
        return ""
        
    def extract_category(self, soup):
        """Extract book category from breadcrumb."""
        breadcrumb = soup.find('ul', class_='breadcrumb')
        if breadcrumb:
            breadcrumb_links = breadcrumb.find_all('a')
            if len(breadcrumb_links) >= 2:  # Skip "Home" and get category
                return breadcrumb_links[-1].get_text(strip=True)
        
        return ""
        
    def extract_upc(self, soup):
        """Extract UPC from product information table."""
        product_table = soup.find('table', class_='table-striped')
        if product_table:
            rows = product_table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 2 and 'UPC' in row.get_text():
                    return cells[1].get_text(strip=True)
        
        return ""
        
    def is_valid_product_url(self, url):
        """Check if URL is a valid book URL."""
        return (url and 
                ('books.toscrape.com' in url) and 
                ('/catalogue/' in url) and
                url.endswith('.html'))
