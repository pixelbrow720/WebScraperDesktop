"""
Chart generator for E-Commerce Data Scraper.
Creates interactive visualizations and statistical charts for scraped data analysis.
"""

import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
import pandas as pd
import numpy as np
from datetime import datetime
import seaborn as sns
from pathlib import Path

from utils.logger import get_logger


class ChartGenerator:
    """Generate various charts and visualizations for scraped data."""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.theme_manager = None
        self.setup_style()
        
    def set_theme_manager(self, theme_manager):
        """Set theme manager for dynamic styling."""
        self.theme_manager = theme_manager
        self.setup_style()
        
    def setup_style(self):
        """Setup matplotlib style for professional-looking charts."""
        # Use a clean, professional style
        plt.style.use('default')
        
        # Get theme colors if theme manager is available
        if self.theme_manager:
            try:
                # Import here to avoid circular imports
                from gui.themes import get_matplotlib_style, get_chart_colors
                
                # Apply theme-specific matplotlib style
                theme_style = get_matplotlib_style(self.theme_manager)
                plt.rcParams.update(theme_style)
                
                # Set theme-specific colors
                self.colors = get_chart_colors(self.theme_manager)
                
            except Exception as e:
                self.logger.warning(f"Could not apply theme to charts: {e}")
                self._setup_default_style()
        else:
            self._setup_default_style()
    
    def _setup_default_style(self):
        """Setup default matplotlib style."""
        # Set default parameters
        plt.rcParams.update({
            'figure.figsize': (10, 6),
            'figure.dpi': 100,
            'figure.facecolor': '#FFFFFF',
            'axes.facecolor': '#FFFFFF',
            'axes.titlesize': 14,
            'axes.labelsize': 12,
            'axes.edgecolor': '#CCCCCC',
            'axes.labelcolor': '#333333',
            'xtick.labelsize': 10,
            'ytick.labelsize': 10,
            'xtick.color': '#666666',
            'ytick.color': '#666666',
            'legend.fontsize': 10,
            'font.family': 'sans-serif',
            'font.sans-serif': ['Arial', 'DejaVu Sans', 'Liberation Sans'],
            'axes.grid': True,
            'grid.alpha': 0.3,
            'grid.color': '#E0E0E0',
            'axes.spines.top': False,
            'axes.spines.right': False,
            'text.color': '#333333'
        })
        
        # Set default color palette
        self.colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#592E83', '#F79D1E']
        
    def generate_chart(self, data, chart_type, save_path=None, **kwargs):
        """
        Generate chart based on type and data.
        
        Args:
            data (pd.DataFrame): Data to visualize
            chart_type (str): Type of chart to generate
            save_path (str): Optional path to save chart
            **kwargs: Additional chart parameters
            
        Returns:
            bool: True if chart generated successfully
        """
        if data.empty:
            self.logger.warning("No data available for visualization")
            return False
            
        try:
            # Clear any existing plots
            plt.clf()
            
            # Generate chart based on type
            if chart_type == 'histogram':
                self._generate_price_histogram(data, **kwargs)
            elif chart_type == 'scatter':
                self._generate_rating_price_scatter(data, **kwargs)
            elif chart_type == 'bar':
                self._generate_top_products_bar(data, **kwargs)
            elif chart_type == 'box':
                self._generate_price_range_box(data, **kwargs)
            elif chart_type == 'category_pie':
                self._generate_category_pie(data, **kwargs)
            elif chart_type == 'rating_distribution':
                self._generate_rating_distribution(data, **kwargs)
            else:
                self.logger.error(f"Unknown chart type: {chart_type}")
                return False
            
            # Save chart if path provided
            if save_path:
                self._save_chart(save_path)
            
            # Show chart
            plt.tight_layout()
            plt.show()
            
            self.logger.info(f"Chart generated successfully: {chart_type}")
            return True
            
        except Exception as e:
            self.logger.error(f"Chart generation failed: {str(e)}")
            return False
            
    def _generate_price_histogram(self, data, **kwargs):
        """Generate price distribution histogram."""
        if 'price' not in data.columns:
            raise ValueError("Price column not found in data")
            
        # Clean and convert price data
        price_data = pd.to_numeric(data['price'], errors='coerce').dropna()
        
        if len(price_data) == 0:
            raise ValueError("No valid price data found")
            
        # Filter out extreme outliers (optional)
        if kwargs.get('filter_outliers', True):
            q1 = price_data.quantile(0.25)
            q3 = price_data.quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            price_data = price_data[(price_data >= lower_bound) & (price_data <= upper_bound)]
        
        # Create histogram
        plt.figure(figsize=(12, 6))
        
        bins = kwargs.get('bins', 30)
        plt.hist(price_data, bins=bins, color=self.colors[0], alpha=0.7, edgecolor='black', linewidth=0.5)
        
        # Add statistics lines
        mean_price = price_data.mean()
        median_price = price_data.median()
        
        plt.axvline(mean_price, color='red', linestyle='--', linewidth=2, label=f'Mean: ${mean_price:.2f}')
        plt.axvline(median_price, color='orange', linestyle='--', linewidth=2, label=f'Median: ${median_price:.2f}')
        
        plt.title('Price Distribution', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Price ($)', fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.legend()
        
        # Add statistics text box
        stats_text = f"""
Statistics:
Count: {len(price_data):,}
Mean: ${mean_price:.2f}
Median: ${median_price:.2f}
Std Dev: ${price_data.std():.2f}
Min: ${price_data.min():.2f}
Max: ${price_data.max():.2f}
"""
        plt.text(0.7, 0.95, stats_text.strip(), transform=plt.gca().transAxes, 
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
    def _generate_rating_price_scatter(self, data, **kwargs):
        """Generate rating vs price scatter plot."""
        if 'price' not in data.columns or 'rating' not in data.columns:
            raise ValueError("Price and/or rating columns not found in data")
            
        # Clean data
        clean_data = data[['price', 'rating']].copy()
        clean_data['price'] = pd.to_numeric(clean_data['price'], errors='coerce')
        clean_data['rating'] = pd.to_numeric(clean_data['rating'], errors='coerce')
        clean_data = clean_data.dropna()
        
        if len(clean_data) == 0:
            raise ValueError("No valid price and rating data found")
            
        plt.figure(figsize=(10, 8))
        
        # Create scatter plot
        plt.scatter(clean_data['price'], clean_data['rating'], 
                   c=self.colors[1], alpha=0.6, s=50, edgecolors='black', linewidth=0.5)
        
        # Add trend line
        if len(clean_data) > 1:
            z = np.polyfit(clean_data['price'], clean_data['rating'], 1)
            p = np.poly1d(z)
            plt.plot(clean_data['price'], p(clean_data['price']), 
                    color='red', linestyle='--', linewidth=2, label='Trend Line')
        
        plt.title('Rating vs Price Correlation', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Price ($)', fontsize=12)
        plt.ylabel('Rating', fontsize=12)
        plt.ylim(0, 5.5)
        
        # Calculate correlation
        correlation = clean_data['price'].corr(clean_data['rating'])
        plt.text(0.05, 0.95, f'Correlation: {correlation:.3f}', 
                transform=plt.gca().transAxes, fontsize=12,
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
        
        if len(clean_data) > 1:
            plt.legend()
            
    def _generate_top_products_bar(self, data, **kwargs):
        """Generate top products bar chart."""
        if 'name' not in data.columns:
            raise ValueError("Product name column not found in data")
            
        # Determine sorting criteria
        sort_by = kwargs.get('sort_by', 'rating')  # 'rating', 'price', or 'name'
        top_n = kwargs.get('top_n', 10)
        
        if sort_by == 'rating' and 'rating' in data.columns:
            # Sort by rating
            sorted_data = data.nlargest(top_n, 'rating')
            y_values = pd.to_numeric(sorted_data['rating'], errors='coerce')
            ylabel = 'Rating'
            title = f'Top {top_n} Products by Rating'
        elif sort_by == 'price' and 'price' in data.columns:
            # Sort by price
            sorted_data = data.nlargest(top_n, 'price')
            y_values = pd.to_numeric(sorted_data['price'], errors='coerce')
            ylabel = 'Price ($)'
            title = f'Top {top_n} Most Expensive Products'
        else:
            # Just show first N products
            sorted_data = data.head(top_n)
            y_values = range(len(sorted_data))
            ylabel = 'Index'
            title = f'First {top_n} Products'
        
        plt.figure(figsize=(12, 8))
        
        # Truncate product names for display
        product_names = [name[:30] + '...' if len(name) > 30 else name 
                        for name in sorted_data['name']]
        
        bars = plt.barh(product_names, y_values, color=self.colors[2], alpha=0.8)
        
        plt.title(title, fontsize=16, fontweight='bold', pad=20)
        plt.xlabel(ylabel, fontsize=12)
        plt.ylabel('Products', fontsize=12)
        
        # Add value labels on bars
        for i, (bar, value) in enumerate(zip(bars, y_values)):
            if pd.notna(value):
                plt.text(value + max(y_values) * 0.01, bar.get_y() + bar.get_height()/2, 
                        f'{value:.2f}', ha='left', va='center', fontsize=10)
        
        plt.gca().invert_yaxis()  # Show highest rated/priced at top
        
    def _generate_price_range_box(self, data, **kwargs):
        """Generate price range box plot."""
        if 'price' not in data.columns:
            raise ValueError("Price column not found in data")
            
        # Clean price data
        price_data = pd.to_numeric(data['price'], errors='coerce').dropna()
        
        if len(price_data) == 0:
            raise ValueError("No valid price data found")
            
        plt.figure(figsize=(8, 6))
        
        # Create box plot
        box_plot = plt.boxplot(price_data, patch_artist=True, labels=['All Products'])
        box_plot['boxes'][0].set_facecolor(self.colors[3])
        box_plot['boxes'][0].set_alpha(0.7)
        
        plt.title('Price Range Analysis', fontsize=16, fontweight='bold', pad=20)
        plt.ylabel('Price ($)', fontsize=12)
        
        # Add statistics
        stats = {
            'Min': price_data.min(),
            'Q1': price_data.quantile(0.25),
            'Median': price_data.median(),
            'Q3': price_data.quantile(0.75),
            'Max': price_data.max(),
            'Mean': price_data.mean(),
            'Std': price_data.std()
        }
        
        stats_text = '\n'.join([f'{k}: ${v:.2f}' for k, v in stats.items()])
        plt.text(1.1, 0.5, stats_text, transform=plt.gca().transAxes, 
                verticalalignment='center', bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
        
    def _generate_category_pie(self, data, **kwargs):
        """Generate category distribution pie chart."""
        if 'category' not in data.columns:
            raise ValueError("Category column not found in data")
            
        # Count categories
        category_counts = data['category'].value_counts()
        
        # Limit to top categories if too many
        max_categories = kwargs.get('max_categories', 8)
        if len(category_counts) > max_categories:
            top_categories = category_counts.head(max_categories - 1)
            others_count = category_counts.iloc[max_categories - 1:].sum()
            category_counts = pd.concat([top_categories, pd.Series({'Others': others_count})])
        
        plt.figure(figsize=(10, 8))
        
        # Create pie chart
        wedges, texts, autotexts = plt.pie(category_counts.values, 
                                          labels=category_counts.index,
                                          autopct='%1.1f%%',
                                          colors=self.colors[:len(category_counts)],
                                          startangle=90,
                                          explode=[0.05] * len(category_counts))
        
        plt.title('Category Distribution', fontsize=16, fontweight='bold', pad=20)
        
        # Improve text readability
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            
    def _generate_rating_distribution(self, data, **kwargs):
        """Generate rating distribution chart."""
        if 'rating' not in data.columns:
            raise ValueError("Rating column not found in data")
            
        # Clean rating data
        rating_data = pd.to_numeric(data['rating'], errors='coerce').dropna()
        
        if len(rating_data) == 0:
            raise ValueError("No valid rating data found")
            
        plt.figure(figsize=(10, 6))
        
        # Create histogram for ratings
        bins = np.arange(0, 6, 0.5)  # 0 to 5 in 0.5 increments
        counts, _, patches = plt.hist(rating_data, bins=bins, color=self.colors[4], 
                                     alpha=0.7, edgecolor='black', linewidth=0.5)
        
        # Color bars based on rating quality
        for i, (patch, count) in enumerate(zip(patches, counts)):
            rating_val = bins[i]
            if rating_val >= 4.5:
                patch.set_facecolor('green')
            elif rating_val >= 4.0:
                patch.set_facecolor('lightgreen')
            elif rating_val >= 3.0:
                patch.set_facecolor('orange')
            else:
                patch.set_facecolor('red')
            patch.set_alpha(0.7)
        
        plt.title('Rating Distribution', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Rating', fontsize=12)
        plt.ylabel('Number of Products', fontsize=12)
        plt.xlim(0, 5)
        
        # Add average rating line
        avg_rating = rating_data.mean()
        plt.axvline(avg_rating, color='red', linestyle='--', linewidth=2, 
                   label=f'Average: {avg_rating:.2f}')
        plt.legend()
        
    def _save_chart(self, filepath):
        """Save chart to file."""
        try:
            # Ensure directory exists
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            
            plt.savefig(filepath, dpi=300, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            
            self.logger.info(f"Chart saved to: {filepath}")
            
        except Exception as e:
            self.logger.error(f"Failed to save chart: {str(e)}")
            
    def generate_statistics(self, data):
        """
        Generate comprehensive statistics for the dataset.
        
        Args:
            data (pd.DataFrame): Data to analyze
            
        Returns:
            str: Formatted statistics report
        """
        if data.empty:
            return "No data available for statistics."
            
        try:
            stats_lines = [
                "DATA STATISTICS REPORT",
                "=" * 50,
                f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "",
                "DATASET OVERVIEW",
                "-" * 20,
                f"Total Records: {len(data):,}",
                f"Total Columns: {len(data.columns)}",
                "",
                "COLUMN SUMMARY",
                "-" * 15,
            ]
            
            # Column information
            for col in data.columns:
                non_null = data[col].count()
                null_count = data[col].isnull().sum()
                null_percentage = (null_count / len(data)) * 100
                
                stats_lines.append(f"{col}:")
                stats_lines.append(f"  - Non-null: {non_null:,} ({100-null_percentage:.1f}%)")
                stats_lines.append(f"  - Data type: {data[col].dtype}")
                
                if col in ['price', 'rating'] and pd.api.types.is_numeric_dtype(data[col]):
                    numeric_data = pd.to_numeric(data[col], errors='coerce').dropna()
                    if len(numeric_data) > 0:
                        stats_lines.extend([
                            f"  - Mean: {numeric_data.mean():.2f}",
                            f"  - Median: {numeric_data.median():.2f}",
                            f"  - Min: {numeric_data.min():.2f}",
                            f"  - Max: {numeric_data.max():.2f}",
                            f"  - Std Dev: {numeric_data.std():.2f}"
                        ])
                
                stats_lines.append("")
            
            # Price analysis
            if 'price' in data.columns:
                price_data = pd.to_numeric(data['price'], errors='coerce').dropna()
                if len(price_data) > 0:
                    stats_lines.extend([
                        "PRICE ANALYSIS",
                        "-" * 15,
                        f"Products with price data: {len(price_data):,}",
                        f"Average price: ${price_data.mean():.2f}",
                        f"Price range: ${price_data.min():.2f} - ${price_data.max():.2f}",
                        f"Median price: ${price_data.median():.2f}",
                        f"Standard deviation: ${price_data.std():.2f}",
                        "",
                        "Price distribution:",
                    ])
                    
                    # Price quartiles
                    quartiles = price_data.quantile([0.25, 0.5, 0.75])
                    stats_lines.extend([
                        f"  - 25th percentile: ${quartiles[0.25]:.2f}",
                        f"  - 50th percentile: ${quartiles[0.5]:.2f}",
                        f"  - 75th percentile: ${quartiles[0.75]:.2f}",
                        ""
                    ])
            
            # Rating analysis
            if 'rating' in data.columns:
                rating_data = pd.to_numeric(data['rating'], errors='coerce').dropna()
                if len(rating_data) > 0:
                    stats_lines.extend([
                        "RATING ANALYSIS",
                        "-" * 16,
                        f"Products with rating data: {len(rating_data):,}",
                        f"Average rating: {rating_data.mean():.2f}/5.0",
                        f"Rating range: {rating_data.min():.1f} - {rating_data.max():.1f}",
                        f"Median rating: {rating_data.median():.2f}",
                        f"Standard deviation: {rating_data.std():.2f}",
                        "",
                        "Rating distribution:",
                    ])
                    
                    # Rating distribution
                    rating_counts = rating_data.value_counts().sort_index()
                    for rating, count in rating_counts.items():
                        percentage = (count / len(rating_data)) * 100
                        stats_lines.append(f"  - {rating:.1f} stars: {count:,} products ({percentage:.1f}%)")
                    
                    stats_lines.append("")
            
            # Category analysis
            if 'category' in data.columns:
                category_counts = data['category'].value_counts()
                if len(category_counts) > 0:
                    stats_lines.extend([
                        "CATEGORY BREAKDOWN",
                        "-" * 18,
                        f"Total categories: {len(category_counts)}",
                        ""
                    ])
                    
                    for category, count in category_counts.head(10).items():
                        percentage = (count / len(data)) * 100
                        stats_lines.append(f"  - {category}: {count:,} ({percentage:.1f}%)")
                    
                    if len(category_counts) > 10:
                        stats_lines.append(f"  ... and {len(category_counts) - 10} more categories")
                    
                    stats_lines.append("")
            
            # Data quality metrics
            total_cells = len(data) * len(data.columns)
            non_null_cells = data.count().sum()
            completeness = (non_null_cells / total_cells) * 100
            
            stats_lines.extend([
                "DATA QUALITY METRICS",
                "-" * 21,
                f"Data completeness: {completeness:.1f}%",
                f"Total data points: {total_cells:,}",
                f"Non-null data points: {non_null_cells:,}",
                f"Missing data points: {total_cells - non_null_cells:,}",
                "",
                "=" * 50
            ])
            
            return '\n'.join(stats_lines)
            
        except Exception as e:
            self.logger.error(f"Statistics generation failed: {str(e)}")
            return f"Error generating statistics: {str(e)}"
            
    def get_available_chart_types(self):
        """Get list of available chart types."""
        return [
            'histogram',
            'scatter', 
            'bar',
            'box',
            'category_pie',
            'rating_distribution'
        ]
