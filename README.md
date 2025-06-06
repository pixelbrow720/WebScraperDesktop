# E-Commerce Data Scraper - Professional Desktop Application

A professional Python desktop application for legal e-commerce data scraping with advanced data export and visualization capabilities. This application is designed for professionals who need to collect and analyze product data from legal sources while maintaining ethical scraping practices.

## 🌟 Key Features

### Core Functionality
- **Professional Desktop GUI** - Modern tkinter-based interface with tabbed layout
- **Customizable Theme System** - 3 built-in themes plus custom theme creation
- **Legal Web Scraping** - Only scrapes from official demo sites with proper rate limiting
- **Multi-Format Export** - Export data to CSV, Excel, and JSON formats
- **Advanced Visualization** - Interactive charts and statistical analysis
- **Real-time Progress Tracking** - Live updates during scraping operations
- **Error Handling & Recovery** - Robust error handling with detailed logging

### Theme System
- **Built-in Themes** - Light, Dark, and Blue Professional themes
- **Custom Theme Creator** - Full color customization with color picker
- **Real-time Theme Switching** - Instant theme changes without restart
- **Auto-save Preferences** - Theme settings persist between sessions
- **Chart Integration** - Visualizations adapt to selected themes

### Data Management
- **Smart Data Processing** - Automatic data cleaning and validation
- **Duplicate Detection** - Advanced duplicate filtering algorithms
- **Price Normalization** - Support for various currencies and formats
- **Rating Standardization** - Consistent rating scales across sources
- **Data Quality Metrics** - Comprehensive data quality reporting

### Advanced Features
- **Rate Limiting** - Configurable request delays and throttling
- **Proxy Support** - Rotation through proxy servers (configurable)
- **Session Management** - Persistent sessions with retry mechanisms
- **Configuration Management** - YAML-based settings with hot reloading
- **Comprehensive Logging** - Detailed operation logs with rotation

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- Windows, macOS, or Linux
- Internet connection for scraping operations

### Installation

1. **Clone repository:**
```bash
git clone https://github.com/yourusername/ecommerce-scraper.git
cd ecommerce-scraper
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Launch application:**
```bash
python main.py
```

Or use the runner script:
```bash
python run.py
```

## 🎨 Theme System

### Built-in Themes
- **Light Theme** - Clean professional appearance for daytime use
- **Dark Theme** - Modern dark interface reducing eye strain
- **Blue Professional** - Corporate-friendly blue-accented theme

### Theme Customization
1. Navigate to **Settings Tab** → **Appearance Section**
2. **Quick Toggle**: Use Dark Mode checkbox for instant switching
3. **Full Customization**: Click "Customize Colors" button to open theme editor
4. **Custom Themes**: Create and save personalized color schemes

### Theme Features
- **Real-time Updates** - Changes apply instantly without restart
- **Auto-save Preferences** - Settings persist between sessions
- **Chart Integration** - Visualizations adapt to selected themes
- **Eight Color Settings** - Background, Text, Buttons, Success, Warning, Error, Selection

## 📖 Usage Guide

### 1. Web Scraping Tab
- Select target website from dropdown (Books to Scrape or Quotes to Scrape)
- Configure scraping parameters:
  - **Max Products**: Maximum products to scrape (1-1000)
  - **Delay**: Request delay in seconds (0.5-10)
  - **Category Filter**: Filter products by category
- Click "Start Scraping" to begin
- Monitor progress through progress bar and status updates

### 2. Data Management Tab
- View summary of scraped data
- Filter data by price and rating ranges
- Export data in multiple formats:
  - **CSV**: For spreadsheets and databases
  - **Excel**: For professional reports with formatting
  - **JSON**: For web applications and APIs

### 3. Visualization Tab
- Create various chart types:
  - **Price Histogram**: Product price distribution
  - **Scatter Plot**: Rating vs price correlation
  - **Bar Chart**: Top-rated products
  - **Box Plot**: Price range analysis
- View comprehensive data statistics
- Save charts to files

### 4. Settings Tab
- Configure user agent and timeout settings
- Set logging levels and output preferences
- **Theme & Appearance**: Theme selection, dark mode toggle, color customization
- Access advanced settings for proxy and rate limiting

## 🎯 Legal Target Sites

### Books to Scrape (http://books.toscrape.com/)
- **Status**: Legal - Demo site designed for scraping practice
- **Data**: 1000+ books with prices, ratings, and categories
- **Categories**: Fiction, Mystery, Romance, Science Fiction, etc.

### Quotes to Scrape (http://quotes.toscrape.com/)
- **Status**: Legal - Demo site designed for scraping practice
- **Data**: Quotes with authors and tags
- **Tags**: Inspirational, Life, Love, Philosophy, etc.

## 📊 Data Output Formats

### Books Data Structure
```json
{
  "name": "Book Title",
  "price": 12.99,
  "rating": 4.5,
  "availability": 22,
  "description": "Book description",
  "category": "Fiction",
  "upc": "a897fe39b1053632",
  "url": "http://books.toscrape.com/catalogue/..."
}
```

### Struktur Data Quotes
```json
{
  "name": "Quote by Author Name",
  "text": "Isi kutipan",
  "author": "Nama Author", 
  "tags": "inspirational, life",
  "rating": 5.0,
  "price": 0.0,
  "category": "Quotes",
  "url": "http://quotes.toscrape.com/..."
}
```

## 🛠️ Fitur Teknis

### Arsitektur Modular
```
src/
├── gui/           # Antarmuka pengguna
│   ├── main_window.py      # Main GUI window
│   ├── dialogs.py          # Progress & settings dialogs
│   ├── themes.py           # Theme management system
│   └── theme_dialog.py     # Theme customization dialog
├── scraper/       # Engine scraping
├── data/          # Pemrosesan & ekspor data
├── visualization/ # Generator grafik
└── utils/         # Utilitas & konfigurasi
```

### Theme System
- **3 Built-in Themes**: Light, Dark, Blue Professional
- **Custom Theme Editor**: Create dan edit custom themes
- **Color Picker**: Customize individual colors
- **Auto-save Preferences**: Theme tersimpan otomatis
- **Chart Integration**: Visualisasi mengikuti theme
- **Real-time Updates**: Perubahan tema langsung terlihat

### Konfigurasi
- **settings.yaml**: Pengaturan aplikasi utama
- **sites.yaml**: Konfigurasi situs target
- **Logging**: Rotasi log otomatis dengan level DEBUG-CRITICAL

### Rate Limiting & Etika
- Delay minimum 0.5 detik antar request
- Maksimal 30 request per menit (default)
- Retry otomatis untuk request gagal
- Respect robots.txt dan terms of service

## 📈 Visualisasi Data

### Jenis Grafik Tersedia
1. **Price Distribution**: Histogram distribusi harga
2. **Rating vs Price**: Scatter plot korelasi
3. **Top Products**: Bar chart produk terbaik
4. **Price Range**: Box plot analisis rentang
5. **Category Pie**: Distribusi kategori
6. **Rating Distribution**: Histogram rating

### Statistik Otomatis
- Mean, median, dan standar deviasi
- Rentang harga (min, max)
- Distribusi rating
- Breakdown kategori
- Metrik kualitas data

## ⚙️ Konfigurasi Lanjutan

### Network Settings
```yaml
network:
  accept_language: "en-US,en;q=0.9"
  accept_encoding: "gzip, deflate, br"
  use_proxy: false
  proxy_url: null
```

### Scraping Parameters
```yaml
scraping:
  default_delay: 1.0
  max_products: 100
  requests_per_minute: 30
  skip_errors: true
  filter_duplicates: true
```

## 🔧 Troubleshooting

### Masalah Umum
1. **Aplikasi tidak start**: Periksa versi Python (minimal 3.11)
2. **Scraping gagal**: Periksa koneksi internet dan delay
3. **Export error**: Pastikan path file valid dan writable
4. **Performance lambat**: Kurangi max products atau tingkatkan delay

### Log Analysis
- File log tersimpan di folder `logs/`
- Format: `ecommerce_scraper_YYYYMMDD_HHMMSS.log`
- Level: DEBUG, INFO, WARNING, ERROR, CRITICAL

## 📄 Lisensi & Legal

Aplikasi ini dirancang khusus untuk:
- Praktek scraping dari situs legal/demo
- Tujuan edukasi dan penelitian
- Mematuhi robots.txt dan rate limiting
- Tidak melanggar terms of service

**PENTING**: Selalu periksa robots.txt dan terms of service sebelum scraping situs baru.

## 🤝 Contributing

1. Fork repository
2. Buat feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📞 Support

- **Documentation**: Lihat folder `docs/` untuk panduan lengkap
- **Issues**: Report bug melalui GitHub Issues
- **Technical**: Baca `TECHNICAL_DOCUMENTATION.md`
- **User Guide**: Baca `USER_MANUAL.md`

## 🎯 Portfolio Features

Aplikasi ini cocok untuk portfolio Upwork karena mendemonstrasikan:

✅ **Desktop Application Development** dengan Python/Tkinter
✅ **Web Scraping** dengan Beautiful Soup dan rate limiting
✅ **Data Processing** dengan Pandas dan validasi
✅ **Data Visualization** dengan Matplotlib/Seaborn
✅ **Professional Documentation** lengkap
✅ **Error Handling** dan logging sistem
✅ **Configuration Management** dengan YAML
✅ **Multi-format Export** (CSV, Excel, JSON)
✅ **Clean Code Architecture** yang modular
✅ **Legal & Ethical Scraping** practices

---

**Version**: 1.0.0  
**Author**: Portfolio Project  
**Python**: 3.11+  
**License**: MIT
