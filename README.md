# Physician Directory Scraper

A comprehensive Streamlit-based web application that fetches physician data from Medifind.com with multiple data source options including authenticated API access, HTML scraping, and sample data generation.

## ✨ Features

### 🔌 **API Integration (Authenticated)**
- Direct access to Medifind API with Bearer token authentication
- Real-time physician data from neuroendocrine tumor specialists
- Configurable search parameters (condition ID, pagination, filters)

### 🌐 **HTML Scraping (BeautifulSoup)**
- Fallback web scraping using BeautifulSoup
- Robust HTML parsing for physician information
- Handles dynamic content and various page structures

### 📊 **Sample Data Generation**
- Realistic sample physician data for demonstration
- Configurable number of physicians (10-100)
- Diverse specialties and geographic distribution

### 🎨 **Interactive Dashboard**
- Beautiful Streamlit interface with modern design
- Real-time filtering and data visualization
- Export functionality (CSV download)
- Detailed physician profiles

## 🏥 Data Fields Extracted

The application extracts comprehensive information for each physician:

- **Personal Information**: Name, Title, Specialty
- **Location**: City, State, Country
- **Professional Metrics**: Years of Experience, Patient Volume, Research Publications, Clinical Trials
- **Contact Information**: Phone, Website, Profile URL
- **Performance**: Ratings, Review Count, Rank Score
- **Additional Details**: Biography, Languages, Insurance Plans, Hospital Affiliations

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Internet connection (for API/scraping modes)

### Installation

1. **Clone or download** the project files
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

#### Option 1: Command Line
```bash
streamlit run sraping.py
```

#### Option 2: Windows Batch File
Double-click `run_streamlit.bat` (Windows only)

#### Option 3: Manual Python
```bash
python -m streamlit run sraping.py
```

## 📖 Usage Guide

### 1. **Choose Data Source**
In the sidebar, select your preferred data source:

- **🔌 API (Authenticated)**: Uses your authentication token for real-time data
- **🌐 HTML Scraping**: BeautifulSoup-based web scraping
- **📊 Sample Data**: Generates realistic demo data

### 2. **Configure Parameters**
- **Condition ID**: 3766 (Neuroendocrine Tumor) or custom
- **Maximum Pages**: Number of pages to fetch
- **Results per Page**: Items per page (API mode only)
- **Sample Size**: Number of demo physicians (Sample mode only)

### 3. **Fetch Data**
Click "🚀 Fetch Physician Data" to start the process

### 4. **Explore Results**
- **📊 Summary Statistics**: Overview metrics
- **🔧 Data Filters**: Filter by state, experience, publications
- **📈 Visualizations**: Interactive charts and graphs
- **📋 Data Table**: Sortable, customizable table view
- **👨‍⚕️ Detailed Profiles**: Individual physician information

### 5. **Export Data**
Use the "📥 Download CSV" button to export filtered results

## 🔧 Configuration

### API Authentication
The application includes a pre-configured Bearer token for API access:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### User Profile
Configured for user: Mustafa Karanjawala (mustafakaranjawala72@gmail.com)

## 📊 Sample Data

When using sample data mode, the application generates realistic physicians with:
- **Diverse Specialties**: Medical Oncology, Endocrine Surgery, Gastroenterology, etc.
- **Top Hospitals**: Memorial Sloan Kettering, MD Anderson, Mayo Clinic, etc.
- **Geographic Distribution**: Major US cities and states
- **Realistic Metrics**: Experience (5-35 years), Publications (0-150), Patient Volume (50-500)

## 🛠️ Technical Details

### Dependencies
- **streamlit**: Web application framework
- **requests**: HTTP library for API calls
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **beautifulsoup4**: HTML parsing
- **plotly**: Interactive visualizations
- **lxml**: XML and HTML parsing

### Architecture
- **Modular Design**: Separate classes for scraping, data processing, and UI
- **Error Handling**: Comprehensive exception handling and user feedback
- **Rate Limiting**: Respectful API usage with delays
- **Caching**: Session state management for performance

## 📈 Visualizations

The application provides multiple interactive visualizations:
- **Experience Distribution**: Histogram of years of experience
- **Geographic Distribution**: Bar chart of physicians by state
- **Experience vs Publications**: Scatter plot with patient volume sizing
- **Performance Metrics**: Rating and review count analysis

## 🚨 Important Notes

### API Limitations
- The Medifind API parameters may change
- Authentication tokens have expiration dates
- Rate limiting may apply to prevent abuse

### Legal Considerations
- Ensure compliance with website terms of service
- Respect robots.txt and rate limiting
- Use data responsibly and ethically

### Sample Data
- Sample data is for demonstration purposes only
- Real physician information should be verified independently
- Do not use sample data for actual medical decisions

## 🔍 Troubleshooting

### Common Issues

1. **API 400 Error**: Try sample data mode for immediate functionality
2. **Empty Results**: Check internet connection and try different data source
3. **Slow Performance**: Reduce page count or use sample data
4. **Missing Packages**: Run `pip install -r requirements.txt`

### Error Messages
- **"Access denied"**: API authentication may have expired
- **"Page appears empty"**: Website structure may have changed
- **"Network error"**: Check internet connection

## 📞 Support

For issues or questions:
- Check the troubleshooting section above
- Verify all dependencies are installed
- Try sample data mode for immediate functionality

## 🎯 Use Cases

- **Medical Research**: Analyze physician specialties and experience
- **Healthcare Analytics**: Study geographic distribution of specialists
- **Data Science Projects**: Practice web scraping and data visualization
- **Educational Purposes**: Learn Streamlit, pandas, and API integration

---

**Note**: This application is for educational and research purposes. Always verify physician information independently and comply with applicable terms of service.
