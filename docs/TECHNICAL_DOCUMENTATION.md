# E-Commerce Data Scraper - Technical Documentation

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Core Components](#core-components)
3. [Theme System](#theme-system)
4. [Data Flow](#data-flow)
5. [API Reference](#api-reference)
6. [Configuration System](#configuration-system)
7. [Extending the Application](#extending-the-application)
8. [Performance Considerations](#performance-considerations)
9. [Security & Compliance](#security--compliance)

## Architecture Overview

### System Architecture

The E-Commerce Data Scraper follows a modular, layered architecture designed for maintainability, extensibility, and robust operation. The application now includes a comprehensive theme system for enhanced user experience.

```
src/
├── gui/                    # User Interface Layer
│   ├── main_window.py     # Main application window with theme integration
│   ├── dialogs.py         # Modal dialogs and popups
│   ├── themes.py          # Theme management system
│   └── theme_dialog.py    # Theme customization interface
├── scraper/               # Data Collection Layer
│   ├── scraper_engine.py  # Main scraping coordinator
│   └── sites/             # Site-specific scrapers
├── data/                  # Data Processing Layer
│   ├── data_processor.py  # Data cleaning and validation
│   └── exporter.py        # Data export functionality
├── visualization/         # Presentation Layer
│   └── chart_generator.py # Chart generation with theme support
└── utils/                 # Utility Layer
    ├── config.py          # Configuration management
    └── logger.py          # Logging functionality
```

### Design Patterns

1. **Model-View-Controller (MVC)**: Separates business logic, UI, and data handling
2. **Observer Pattern**: Theme changes notify all UI components
3. **Strategy Pattern**: Different scraping strategies for different sites
4. **Factory Pattern**: Dynamic creation of scrapers and exporters
5. **Singleton Pattern**: Configuration and theme managers

## Core Components

### GUI Layer (`src/gui/`)

#### MainWindow (`main_window.py`)
- Primary application interface with tabbed navigation
- Integrated theme management and real-time theme switching
- Handles user interactions and coordinates with other components
- Implements responsive design that adapts to different themes

#### Theme System (`themes.py`, `theme_dialog.py`)
- **ThemeManager**: Central theme management with 3 built-in themes
- **ThemedWidget**: Base class for theme-aware widgets
- **ThemeDialog**: Color customization interface with live preview
- **Auto-save**: Theme preferences persist across sessions

### Scraper Layer (`src/scraper/`)

#### ScraperEngine (`scraper_engine.py`)
- Coordinates all scraping operations with rate limiting
- Manages HTTP sessions with retry mechanisms
- Implements ethical scraping practices and compliance

#### Site-Specific Scrapers (`sites/`)
- Modular scrapers for different e-commerce platforms
- Books to Scrape and Quotes to Scrape implementations
- Extensible architecture for adding new sites

### Data Processing Layer (`src/data/`)

#### DataProcessor (`data_processor.py`)
- Cleans and validates scraped data
- Handles price normalization and rating standardization
- Implements duplicate detection and data quality metrics

#### DataExporter (`exporter.py`)
- Multi-format export (CSV, Excel, JSON)
- Professional formatting with metadata
- Theme-aware export styling for Excel files

### Visualization Layer (`src/visualization/`)

#### ChartGenerator (`chart_generator.py`)
- Theme-aware chart generation using matplotlib
- Multiple chart types: histogram, scatter, bar, box plots
- Dynamic color schemes that adapt to selected theme
- Professional statistical analysis and presentation

### Utility Layer (`src/utils/`)

#### Configuration (`config.py`)
- YAML-based configuration management
- Theme preferences and appearance settings
- Runtime configuration updates and persistence

#### Logging (`logger.py`)
- Comprehensive logging with rotation
- Configurable log levels and file management
- Integration with all application components

## Theme System

### Architecture

The theme system provides a comprehensive theming solution that affects all visual aspects of the application:

```python
# Theme Manager Structure
ThemeManager
├── Built-in Themes
│   ├── Light Theme (default)
│   ├── Dark Theme
│   └── Blue Professional
├── Custom Themes
│   ├── User-created themes
│   └── Persistent storage
└── Theme Application
    ├── GUI Components
    ├── Chart Styling
    └── Real-time Updates
```

### Implementation Details

#### Theme Configuration
```yaml
# settings.yaml
appearance:
  theme: "light"                    # Current theme
  auto_switch_dark_mode: false      # Auto dark mode
  dark_mode_start_time: "20:00"     # Auto switch time
  dark_mode_end_time: "06:00"       # Auto switch time
  font_family: "default"            # Font preferences
  font_size: 10                     # UI font size
```

#### Color System
Each theme defines a comprehensive color palette:
- **Primary Colors**: Background, text, borders
- **Button Colors**: Primary, secondary, success, danger
- **Status Colors**: Success, warning, error, info
- **Chart Colors**: Consistent visualization palette
- **Selection Colors**: UI selection and highlighting

#### Theme Integration Points
1. **Main Window**: All UI components themed recursively
2. **Charts**: Matplotlib styling adapts to theme colors
3. **Dialogs**: Progress and settings dialogs themed
4. **Export**: Excel formatting uses theme colors
5. **Real-time**: Theme changes apply immediately

### Custom Theme Creation

Users can create custom themes through the Theme Dialog:
1. Select base theme (Light, Dark, Blue)
2. Customize individual colors using color picker
3. Preview changes in real-time
4. Save as named custom theme
5. Auto-save preferences

## Data Flow

### Scraping Workflow

```
User Input → Site Selection → Configuration
     ↓
Rate Limiter → HTTP Session → Site Scraper
     ↓
Raw Data → Data Processor → Validation
     ↓
Clean Data → Storage → UI Display
```

### Theme Application Flow

```
Theme Selection → ThemeManager → Color Palette
     ↓
GUI Components ← Theme Application ← Configuration
     ↓
Chart Generator ← Style Updates ← Matplotlib
     ↓
Auto-save → Config File → Persistence
```

### Export Workflow

```
Processed Data → Format Selection → Exporter
     ↓
Theme Colors → Formatting → File Generation
     ↓
Metadata → Quality Report → User Notification
```

## API Reference

### Theme System API

#### ThemeManager Class

```python
class ThemeManager:
    def __init__(self)
    def get_available_themes(self) -> Dict[str, str]
    def set_theme(self, theme_id: str) -> bool
    def get_color(self, color_key: str) -> str
    def is_dark_theme(self) -> bool
    def create_custom_theme(self, theme_id: str, theme_name: str, base_theme: str) -> bool
```

#### ThemedWidget Class

```python
class ThemedWidget:
    def __init__(self, theme_manager: ThemeManager)
    def apply_theme(self, widget, widget_type: str = "default")
```

#### Chart Integration

```python
def setup_style(self):
    """Apply theme to matplotlib configuration"""
    
def get_matplotlib_style(theme_manager: ThemeManager) -> Dict[str, Any]:
    """Get theme-specific matplotlib style"""
    
def get_chart_colors(theme_manager: ThemeManager) -> list:
    """Get theme-specific color palette"""
```

### Configuration API

```python
# Theme configuration access
config.get_setting("appearance", "theme", "light")
config.set_setting("appearance", "theme", "dark")
config.save_settings()
```

## Configuration System

### File Structure

```
config/
├── settings.yaml          # Main application settings
├── sites.yaml            # Site-specific configurations
└── custom_themes.json    # User-created themes
```

### Theme Configuration

```yaml
appearance:
  theme: "light"                    # Active theme
  auto_switch_dark_mode: false      # Automatic switching
  dark_mode_start_time: "20:00"     # Evening switch
  dark_mode_end_time: "06:00"       # Morning switch
  font_family: "default"            # UI font
  font_size: 10                     # Font size
  transparency: 100                 # Window transparency
  always_on_top: false              # Window behavior
```

## Extending the Application

### Adding New Themes

1. **Built-in Theme**: Add to `themes.py` default themes dictionary
2. **Custom Theme**: Use ThemeDialog or programmatically create
3. **Color Palette**: Define all required color keys
4. **Testing**: Verify all UI components respond correctly

### Creating Custom Scrapers

```python
class CustomSiteScraper(BaseScraper):
    def __init__(self, config):
        super().__init__(config)
        
    def scrape_products(self, max_products=100):
        # Implementation with theme-aware progress reporting
        pass
```

### Extending Chart Types

```python
def generate_custom_chart(self, data, **kwargs):
    # Apply current theme
    self.setup_style()
    
    # Use theme colors
    colors = self.colors
    
    # Create chart with theme integration
    pass
```

## Performance Considerations

### Theme System Performance

1. **Lazy Loading**: Themes loaded only when needed
2. **Caching**: Color calculations cached for performance
3. **Batch Updates**: UI updates batched for smooth transitions
4. **Memory Management**: Efficient theme object management

### UI Responsiveness

1. **Background Threading**: Non-blocking theme application
2. **Progressive Updates**: UI components updated incrementally
3. **Efficient Redraws**: Minimize unnecessary widget refreshes

## Security & Compliance

### Theme Security

1. **Input Validation**: Color values validated before application
2. **File Permissions**: Secure custom theme file storage
3. **Configuration Safety**: Protected configuration access

### Data Privacy

1. **No External Calls**: Theme system operates entirely offline
2. **Local Storage**: All preferences stored locally
3. **User Control**: Complete user control over appearance settings

The theme system enhances user experience while maintaining the application's professional standards and performance characteristics.
