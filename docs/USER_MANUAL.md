# E-Commerce Data Scraper - User Manual

## Table of Contents
1. [Getting Started](#getting-started)
2. [Interface Overview](#interface-overview)
3. [Theme System](#theme-system)
4. [Web Scraping](#web-scraping)
5. [Data Management](#data-management)
6. [Visualization](#visualization)
7. [Settings & Configuration](#settings--configuration)
8. [Troubleshooting](#troubleshooting)
9. [Best Practices](#best-practices)

## Getting Started

### System Requirements
- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: Version 3.8 or higher
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 500MB free space
- **Network**: Internet connection for scraping operations

### Installation

1. **Download the application** from the official repository
2. **Extract files** to your preferred directory
3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Launch the application**:
   ```bash
   python main.py
   ```

### First Launch

When you first run the application:
1. Configuration files are automatically created
2. Default settings are applied
3. The main window opens with an empty interface
4. All features are immediately available

## Interface Overview

### Main Window Layout

The application uses a modern tabbed interface with four main sections:

#### 1. Web Scraping Tab
- **Purpose**: Configure and execute scraping operations
- **Key Components**:
  - Website selection dropdown
  - Scraping parameters (max products, delay, filters)
  - Control buttons (Start/Stop)
  - Progress tracking
  - Results preview table

#### 2. Data Management Tab
- **Purpose**: View, filter, and export scraped data
- **Key Components**:
  - Data summary statistics
  - Export format selection
  - Data filtering options
  - Export buttons

#### 3. Visualization Tab
- **Purpose**: Create charts and analyze data
- **Key Components**:
  - Chart type selection
  - Generate chart button
  - Statistics display area
  - Chart viewing area

#### 4. Settings Tab
- **Purpose**: Configure application behavior
- **Key Components**:
  - General settings
  - Network configuration
  - Advanced options
  - Save/Reset buttons

### Status Bar
Located at the bottom of the window:
- Shows current application status
- Displays progress indicators during operations
- Provides real-time feedback

## Theme System

### Overview
The application includes a comprehensive theme system that allows you to customize the visual appearance to match your preferences. You can choose from built-in themes or create your own custom themes.

### Available Themes

#### Built-in Themes
1. **Light Theme** (Default)
   - Clean white background with dark text
   - Professional appearance suitable for daytime use
   - High contrast for excellent readability

2. **Dark Theme**
   - Dark background with light text
   - Reduces eye strain in low-light conditions
   - Modern appearance preferred by many users

3. **Blue Professional**
   - Blue-accented professional theme
   - Corporate-friendly appearance
   - Balanced colors for extended use

### Accessing Theme Settings

#### Quick Access - Dark Mode Toggle
1. Navigate to the **Settings tab**
2. In the **Appearance section**, find the **Dark Mode** checkbox
3. Check the box to switch to dark theme instantly
4. Uncheck to return to light theme

#### Full Theme Selection
1. Navigate to the **Settings tab**
2. In the **Appearance section**, find the **Theme** dropdown
3. Select from available themes:
   - light
   - dark
   - blue
   - Any custom themes you've created

### Customizing Themes

#### Opening the Theme Customization Dialog
1. Navigate to the **Settings tab**
2. Click the **"Customize Colors"** button
3. The Theme Customization Dialog will open

#### Using the Theme Dialog

**Preview Section**
- Shows sample widgets with current theme applied
- Changes update in real-time as you modify colors
- Includes tabs showing different interface elements

**Color Customization**
- Eight key color settings available:
  - Background
  - Text
  - Primary Button
  - Secondary Button
  - Success
  - Warning
  - Error
  - Selection

**Changing Colors**
1. Click any colored button next to a color name
2. Color picker dialog will open
3. Select your desired color
4. Preview updates immediately
5. Click OK to apply or Cancel to revert

**Saving Custom Themes**
1. After customizing colors, click **"Save as Custom Theme"**
2. Enter a name for your theme
3. Your theme will be added to the theme dropdown
4. Custom themes are automatically saved and persist between sessions

#### Theme Dialog Controls
- **Apply**: Apply changes without closing dialog
- **OK**: Apply changes and close dialog
- **Cancel**: Discard changes and close dialog
- **Reset to Default**: Restore current theme to its original colors

### Theme Features

#### Auto-Save
- Your theme preference is automatically saved
- The selected theme will be restored when you restart the application
- Custom theme modifications are preserved

#### Real-Time Updates
- Theme changes apply immediately throughout the application
- All tabs, dialogs, and windows update instantly
- Charts and visualizations adapt to the new color scheme

#### Chart Integration
- Data visualizations automatically use theme colors
- Charts maintain readability across all themes
- Color palettes adjust to complement the selected theme

### Best Practices

#### Creating Custom Themes
1. Start with a base theme that's close to your preference
2. Make incremental color changes rather than dramatic shifts
3. Test readability by viewing different tabs
4. Consider contrast ratios for accessibility

#### Theme Selection Tips
- Use **Light Theme** for bright environments and daytime work
- Use **Dark Theme** for low-light conditions and evening use
- Use **Blue Professional** for corporate or presentation environments
- Create custom themes for specific workflows or branding needs

#### Accessibility Considerations
- Ensure sufficient contrast between text and background colors
- Test custom themes with different interface elements
- Consider colorblind-friendly color combinations

### Troubleshooting Theme Issues

#### Theme Not Applying
1. Ensure you clicked "Apply" or "OK" in the theme dialog
2. Check that the correct theme is selected in the dropdown
3. Restart the application if changes don't appear

#### Custom Theme Lost
- Custom themes are saved in `config/custom_themes.json`
- If this file is deleted, custom themes will be lost
- Regular backups of the config folder are recommended

#### Colors Look Wrong
1. Verify your monitor's color calibration
2. Check if system-wide color filters are active
3. Try switching to a different theme and back

## Web Scraping

### Selecting a Website

1. **Open the Web Scraping tab**
2. **Click the "Select Website" dropdown**
3. **Choose from available options**:
   - Books to Scrape (Demo bookstore)
   - Quotes to Scrape (Demo quotes site)
4. **Review site information** displayed below the dropdown

### Configuring Scraping Parameters

#### Max Products
- **Range**: 1 to 1000
- **Default**: 50
- **Purpose**: Limits the number of products to scrape
- **Tip**: Start with smaller numbers for testing

#### Delay Between Requests
- **Range**: 0.5 to 10.0 seconds
- **Default**: 1.0 second
- **Purpose**: Prevents overloading target servers
- **Legal Requirement**: Maintains ethical scraping practices

#### Category Filter
- **Format**: Text string
- **Purpose**: Filters products by category/tag
- **Examples**:
  - "Fiction" (for books)
  - "inspirational" (for quotes)
- **Note**: Case-insensitive matching

### Starting a Scraping Session

1. **Configure all parameters**
2. **Click "Start Scraping"**
3. **Monitor progress** in the progress bar
4. **View real-time status** in the status label
5. **See results** appear in the preview table

#### During Scraping
- Progress bar shows completion percentage
- Status label displays current activity
- Results appear in real-time
- Stop button becomes available

#### Stopping Scraping
- **Click "Stop Scraping"** to halt the process
- **Data collected so far is preserved**
- **Partial results are still usable**

### Understanding Results

The results preview table shows:
- **Product Name**: Item title or description
- **Price**: Formatted price (may be $0.00 for free items)
- **Rating**: Numerical rating (1-5 scale)
- **URL**: Source webpage link

## Data Management

### Viewing Data Summary

The data summary section displays:
- **Total products** scraped
- **Price range** (min, max, average)
- **Average rating**
- **Data quality indicators**

### Filtering Data

#### Price Range Filter
1. **Enter minimum price** (optional)
2. **Enter maximum price** (optional)
3. **Click "Apply Filters"**
4. **View filtered results** in the table

#### Rating Filter
1. **Set minimum rating** using the spinner
2. **Click "Apply Filters"**
3. **Results show only items** meeting the criteria

### Exporting Data

#### Export Formats

**CSV (Comma-Separated Values)**
- Best for: Excel, database imports
- Features: UTF-8 encoding, configurable delimiters
- File size: Smallest

**Excel (XLSX)**
- Best for: Professional reports, presentations
- Features: Formatted headers, auto-sized columns, metadata sheet
- File size: Medium

**JSON (JavaScript Object Notation)**
- Best for: Programming, web applications
- Features: Structured data, metadata included
- File size: Medium

#### Export Process

1. **Choose export format** using radio buttons
2. **Select data scope**:
   - "Export All Data": Complete dataset
   - "Export Selected": Only selected table rows
3. **Click appropriate export button**
4. **Choose destination file** in the dialog
5. **Confirm export completion** in the success message

### Export Options

#### CSV Options
- **Delimiter**: Comma, semicolon, or tab
- **Headers**: Include/exclude column headers
- **Encoding**: UTF-8 with BOM for Excel compatibility

#### Excel Options
- **Sheet naming**: Automatic based on data source
- **Formatting**: Professional headers and styling
- **Metadata**: Separate sheet with export information

#### JSON Options
- **Structure**: Hierarchical with metadata
- **Formatting**: Pretty-printed for readability
- **Encoding**: UTF-8 for international characters

## Visualization

### Chart Types

#### Price Distribution (Histogram)
- **Purpose**: Shows how prices are distributed
- **Features**: Mean/median lines, statistics box
- **Best for**: Understanding price ranges

#### Rating vs Price (Scatter Plot)
- **Purpose**: Shows correlation between rating and price
- **Features**: Trend line, correlation coefficient
- **Best for**: Finding value-for-money products

#### Top Products (Bar Chart)
- **Purpose**: Shows highest-rated or most expensive items
- **Features**: Horizontal bars, value labels
- **Best for**: Identifying standout products

#### Price Range Analysis (Box Plot)
- **Purpose**: Shows price distribution with quartiles
- **Features**: Outlier detection, statistical summary
- **Best for**: Understanding price spread

### Generating Charts

1. **Ensure data is loaded** (scrape or import data first)
2. **Go to Visualization tab**
3. **Select chart type** using radio buttons
4. **Click "Generate Chart"**
5. **View chart** in a new window
6. **Optionally save chart** to file

### Statistics Display

The statistics area shows:
- **Dataset overview** (records, columns)
- **Column information** (data types, missing values)
- **Price analysis** (if price data available)
- **Rating analysis** (if rating data available)
- **Category breakdown** (if category data available)
- **Data quality metrics**

#### Updating Statistics
- **Click "Update Statistics"** to refresh the display
- **Statistics automatically update** after new scraping
- **Includes data quality assessment**

## Settings & Configuration

### General Settings

#### User Agent
- **Purpose**: Identifies the application to websites
- **Default**: Chrome browser string
- **Recommendation**: Keep default unless required

#### Logging Level
- **Options**: DEBUG, INFO, WARNING, ERROR
- **Default**: INFO
- **Purpose**: Controls log detail level

#### Network Settings

**Request Timeout**
- **Range**: 5 to 120 seconds
- **Default**: 30 seconds
- **Purpose**: Maximum wait time for responses

**Max Retry Attempts**
- **Range**: 1 to 10
- **Default**: 3
- **Purpose**: Number of retries for failed requests

### Advanced Settings

Access advanced settings through the dedicated dialog:

#### Network Configuration
- **Accept-Language**: Browser language preferences
- **Accept-Encoding**: Compression preferences
- **Proxy Settings**: Optional proxy configuration

#### Rate Limiting
- **Requests per Minute**: Maximum request frequency
- **Random Delay Range**: Min/max delay between requests
- **Purpose**: Prevents server overload

#### Error Handling
- **Skip Errors**: Continue on individual product errors
- **Log Errors**: Record all errors for analysis

### Saving Settings

1. **Modify settings** as needed
2. **Click "Save Settings"** to persist changes
3. **Settings apply immediately** to new operations
4. **Use "Reset to Defaults"** to restore original values

## Troubleshooting

### Common Issues

#### Application Won't Start
**Symptoms**: Error messages, crashes on startup
**Solutions**:
1. Check Python version (requires 3.8+)
2. Install missing dependencies: `pip install -r requirements.txt`
3. Check console for specific error messages
4. Verify file permissions in application directory

#### Scraping Fails Immediately
**Symptoms**: "Failed to scrape" error, no data collected
**Solutions**:
1. Check internet connection
2. Verify target website is accessible
3. Review rate limiting settings (try higher delays)
4. Check logs for detailed error information

#### No Data Appears
**Symptoms**: Scraping completes but table is empty
**Solutions**:
1. Check category filter (may be too restrictive)
2. Verify website has products in selected category
3. Increase max products setting
4. Review logs for parsing errors

#### Export Failures
**Symptoms**: "Export failed" error message
**Solutions**:
1. Ensure target directory exists and is writable
2. Check available disk space
3. Close any open files with the same name
4. Try different export location

#### Poor Performance
**Symptoms**: Slow scraping, application freezes
**Solutions**:
1. Increase delay between requests
2. Reduce max products setting
3. Close other applications to free memory
4. Check network connection speed

### Log Analysis

#### Viewing Logs
1. **Navigate to logs/ directory**
2. **Open most recent log file**
3. **Search for ERROR or WARNING entries**
4. **Review timestamps** to correlate with issues

#### Log Levels
- **DEBUG**: Detailed execution information
- **INFO**: General operational messages
- **WARNING**: Potential issues that don't stop execution
- **ERROR**: Problems that prevent specific operations
- **CRITICAL**: Severe errors that may stop the application

### Getting Help

#### Self-Help Resources
1. **Check this manual** for solutions
2. **Review log files** for error details
3. **Verify configuration** against documentation
4. **Test with minimal settings** (small max products, high delay)

#### Reporting Issues
When reporting problems, include:
1. **Exact error messages**
2. **Steps to reproduce the issue**
3. **Configuration settings used**
4. **Relevant log file excerpts**
5. **System information** (OS, Python version)

## Best Practices

### Ethical Scraping

#### Respect Rate Limits
- **Use appropriate delays** (1+ seconds recommended)
- **Don't scrape during peak hours**
- **Monitor server response times**
- **Stop if servers seem overloaded**

#### Legal Compliance
- **Only scrape authorized sites** (like included demo sites)
- **Check robots.txt** before adding new sites
- **Review terms of service**
- **Respect copyright and data ownership**

### Performance Optimization

#### Efficient Data Collection
- **Start with small batches** to test parameters
- **Use category filters** to target specific data
- **Avoid duplicate scraping** of same data
- **Monitor memory usage** during large operations

#### Data Management
- **Regular exports** prevent data loss
- **Use appropriate file formats** for your needs
- **Clean up old log files** periodically
- **Back up configuration** files

### Quality Assurance

#### Data Validation
- **Review sample results** before large operations
- **Check data quality metrics** after scraping
- **Validate exported files** in target applications
- **Monitor for missing or malformed data**

#### Error Prevention
- **Test with minimal settings** first
- **Keep software updated**
- **Monitor log files** for warnings
- **Maintain stable network connection**

### Workflow Recommendations

#### Daily Use
1. **Start with conservative settings**
2. **Monitor first few results** for quality
3. **Adjust parameters** based on initial results
4. **Export data regularly** to prevent loss
5. **Review logs** for any issues

#### Large Projects
1. **Plan scraping in phases**
2. **Test extensively** with small samples
3. **Use category filters** to organize data
4. **Export in multiple formats** for different uses
5. **Document settings** used for reproducibility

---

This manual covers the essential aspects of using the E-Commerce Data Scraper. For additional technical details, see the Technical Documentation. For support, consult the troubleshooting section or contact support.
