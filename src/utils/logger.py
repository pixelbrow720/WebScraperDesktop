"""
Logging configuration and utilities for E-Commerce Data Scraper.
Provides structured logging with file output and console display.
"""

import logging
import logging.handlers
import os
import sys
from datetime import datetime
from pathlib import Path


class ColoredFormatter(logging.Formatter):
    """Custom formatter that adds colors to console output."""
    
    # Color codes
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record):
        """Format log record with colors."""
        # Add color to level name
        level_color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        record.levelname = f"{level_color}{record.levelname}{self.COLORS['RESET']}"
        
        # Format the message
        return super().format(record)


def setup_logging(log_level='INFO', log_file=None, console_output=True):
    """
    Setup application logging configuration.
    
    Args:
        log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file (str): Optional log file path
        console_output (bool): Whether to output to console
    """
    # Create logs directory if it doesn't exist
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    # Set log file path if not provided
    if log_file is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = log_dir / f'ecommerce_scraper_{timestamp}.log'
    
    # Convert string level to logging constant
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Clear any existing handlers
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Configure root logger
    root_logger.setLevel(numeric_level)
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_formatter = ColoredFormatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # File handler with rotation
    if log_file:
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
    
    # Console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(numeric_level)
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)
    
    # Log setup completion
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized - Level: {log_level}, File: {log_file}")
    
    return str(log_file)


def get_logger(name):
    """
    Get a logger instance for a specific module.
    
    Args:
        name (str): Logger name (usually __name__)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    return logging.getLogger(name)


class PerformanceLogger:
    """Context manager for logging performance metrics."""
    
    def __init__(self, operation_name, logger=None):
        self.operation_name = operation_name
        self.logger = logger or get_logger(__name__)
        self.start_time = None
        
    def __enter__(self):
        self.start_time = datetime.now()
        self.logger.info(f"Starting operation: {self.operation_name}")
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time:
            duration = datetime.now() - self.start_time
            duration_seconds = duration.total_seconds()
            
            if exc_type is None:
                self.logger.info(f"Operation completed: {self.operation_name} (Duration: {duration_seconds:.2f}s)")
            else:
                self.logger.error(f"Operation failed: {self.operation_name} (Duration: {duration_seconds:.2f}s)")


class LogAnalyzer:
    """Utility class for analyzing log files."""
    
    def __init__(self, log_file_path):
        self.log_file_path = Path(log_file_path)
        self.logger = get_logger(__name__)
        
    def get_log_summary(self):
        """Get summary statistics from log file."""
        if not self.log_file_path.exists():
            return {"error": "Log file not found"}
        
        try:
            with open(self.log_file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            summary = {
                'total_lines': len(lines),
                'log_levels': {'DEBUG': 0, 'INFO': 0, 'WARNING': 0, 'ERROR': 0, 'CRITICAL': 0},
                'modules': {},
                'first_entry': None,
                'last_entry': None,
                'errors': []
            }
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Extract timestamp
                if ' | ' in line:
                    parts = line.split(' | ')
                    if len(parts) >= 4:
                        timestamp, module, level, message = parts[0], parts[1], parts[2], ' | '.join(parts[3:])
                        
                        # Set first/last entry
                        if summary['first_entry'] is None:
                            summary['first_entry'] = timestamp
                        summary['last_entry'] = timestamp
                        
                        # Count log levels
                        if level in summary['log_levels']:
                            summary['log_levels'][level] += 1
                        
                        # Count modules
                        if module not in summary['modules']:
                            summary['modules'][module] = 0
                        summary['modules'][module] += 1
                        
                        # Collect errors
                        if level in ['ERROR', 'CRITICAL']:
                            summary['errors'].append({
                                'timestamp': timestamp,
                                'level': level,
                                'module': module,
                                'message': message
                            })
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Error analyzing log file: {str(e)}")
            return {"error": str(e)}
    
    def get_recent_errors(self, count=10):
        """Get recent errors from log file."""
        summary = self.get_log_summary()
        if 'error' in summary:
            return summary
        
        errors = summary.get('errors', [])
        return errors[-count:] if len(errors) > count else errors
    
    def export_log_report(self, output_path):
        """Export log analysis report."""
        try:
            summary = self.get_log_summary()
            if 'error' in summary:
                return False
            
            report_lines = [
                "LOG ANALYSIS REPORT",
                "=" * 40,
                f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                f"Log File: {self.log_file_path}",
                "",
                "SUMMARY STATISTICS",
                "-" * 20,
                f"Total Log Entries: {summary['total_lines']:,}",
                f"First Entry: {summary['first_entry']}",
                f"Last Entry: {summary['last_entry']}",
                "",
                "LOG LEVEL BREAKDOWN",
                "-" * 20,
            ]
            
            for level, count in summary['log_levels'].items():
                percentage = (count / summary['total_lines'] * 100) if summary['total_lines'] > 0 else 0
                report_lines.append(f"{level}: {count:,} ({percentage:.1f}%)")
            
            report_lines.extend([
                "",
                "TOP MODULES",
                "-" * 12,
            ])
            
            # Sort modules by count
            sorted_modules = sorted(summary['modules'].items(), key=lambda x: x[1], reverse=True)
            for module, count in sorted_modules[:10]:
                percentage = (count / summary['total_lines'] * 100) if summary['total_lines'] > 0 else 0
                report_lines.append(f"{module}: {count:,} ({percentage:.1f}%)")
            
            if summary['errors']:
                report_lines.extend([
                    "",
                    "RECENT ERRORS",
                    "-" * 13,
                ])
                
                for error in summary['errors'][-5:]:  # Last 5 errors
                    report_lines.extend([
                        f"Time: {error['timestamp']}",
                        f"Level: {error['level']}",
                        f"Module: {error['module']}",
                        f"Message: {error['message']}",
                        ""
                    ])
            
            # Write report
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(report_lines))
            
            self.logger.info(f"Log analysis report exported to: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to export log report: {str(e)}")
            return False


# Custom log handlers for specific use cases
class ScrapingProgressHandler(logging.Handler):
    """Custom handler for tracking scraping progress."""
    
    def __init__(self, progress_callback=None):
        super().__init__()
        self.progress_callback = progress_callback
        self.scraping_stats = {
            'requests_made': 0,
            'items_scraped': 0,
            'errors_occurred': 0
        }
    
    def emit(self, record):
        """Process log record and update progress."""
        try:
            message = record.getMessage().lower()
            
            # Track different types of events
            if 'request' in message or 'scraping' in message:
                self.scraping_stats['requests_made'] += 1
            
            if 'scraped' in message or 'extracted' in message:
                self.scraping_stats['items_scraped'] += 1
            
            if record.levelno >= logging.ERROR:
                self.scraping_stats['errors_occurred'] += 1
            
            # Call progress callback if provided
            if self.progress_callback:
                self.progress_callback(self.scraping_stats)
                
        except Exception:
            pass  # Don't let logging errors break the application
    
    def get_stats(self):
        """Get current scraping statistics."""
        return self.scraping_stats.copy()
    
    def reset_stats(self):
        """Reset scraping statistics."""
        self.scraping_stats = {
            'requests_made': 0,
            'items_scraped': 0,
            'errors_occurred': 0
        }


def setup_scraping_logger(progress_callback=None):
    """Setup logger specifically for scraping operations."""
    logger = get_logger('scraping')
    
    # Add progress handler
    progress_handler = ScrapingProgressHandler(progress_callback)
    progress_handler.setLevel(logging.INFO)
    logger.addHandler(progress_handler)
    
    return logger, progress_handler
