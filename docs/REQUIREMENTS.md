# Dependencies & Requirements

## Python Version
- **Minimum**: Python 3.11
- **Recommended**: Python 3.11+ (latest stable)

## Core Dependencies

### Web Scraping
```
requests>=2.32.3          # HTTP library for making requests
beautifulsoup4>=4.13.4    # HTML/XML parsing
trafilatura>=2.0.0        # Text extraction from web pages
```

### Data Processing
```
pandas>=2.3.0             # Data analysis and manipulation
numpy>=1.24.0             # Numerical computing
```

### Visualization
```
matplotlib>=3.10.3        # Plotting library
seaborn>=0.13.2          # Statistical visualization
```

### File Handling
```
openpyxl>=3.1.5          # Excel file support
pyyaml>=6.0.2            # YAML configuration files
```

### GUI Framework
```
tkinter                   # Desktop GUI (included with Python)
```

## Installation Commands

### Using pip (recommended):
```bash
pip install requests beautifulsoup4 pandas matplotlib seaborn pyyaml openpyxl trafilatura
```

### Or install individually:
```bash
pip install requests>=2.32.3
pip install beautifulsoup4>=4.13.4
pip install pandas>=2.3.0
pip install matplotlib>=3.10.3
pip install seaborn>=0.13.2
pip install pyyaml>=6.0.2
pip install openpyxl>=3.1.5
pip install trafilatura>=2.0.0
```

## System Requirements

### Operating System
- Windows 10 or later
- macOS 10.14 or later
- Linux (Ubuntu 18.04+ or equivalent)

### Hardware
- **RAM**: Minimum 4GB, Recommended 8GB+
- **Storage**: 500MB free space
- **Network**: Internet connection for scraping operations

### Python Environment
- Standard library modules (included with Python):
  - tkinter (GUI framework)
  - threading (concurrent operations)
  - json (JSON handling)
  - csv (CSV file handling)
  - urllib (URL handling)
  - re (regular expressions)
  - datetime (date/time operations)
  - pathlib (path operations)
  - logging (logging system)

## Verification

To verify all dependencies are installed correctly:

```python
# Run this script to check dependencies
import sys

def check_dependencies():
    dependencies = [
        'requests', 'bs4', 'pandas', 'matplotlib', 
        'seaborn', 'yaml', 'openpyxl', 'trafilatura'
    ]
    
    missing = []
    for dep in dependencies:
        try:
            if dep == 'bs4':
                import bs4
            elif dep == 'yaml':
                import yaml
            else:
                __import__(dep)
            print(f"✓ {dep}")
        except ImportError:
            missing.append(dep)
            print(f"✗ {dep}")
    
    if missing:
        print(f"\nMissing dependencies: {', '.join(missing)}")
        return False
    else:
        print("\nAll dependencies satisfied!")
        return True

if __name__ == "__main__":
    check_dependencies()
```

## Development Dependencies (Optional)

For development and testing:
```bash
pip install pytest pytest-cov black flake8
```

## Notes

- All dependencies are compatible with Python 3.11+
- Version constraints ensure reproducible builds
- No unnecessary dependencies - lightweight application
- All packages available via pip
- GUI uses tkinter (included with Python standard library)