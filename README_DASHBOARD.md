# Restaurant Sales Analytics Dashboard

## Overview
A comprehensive Streamlit web application for analyzing restaurant sales data with enhanced visualizations and interactive features.

## Features

### 📊 Key Performance Indicators
- Total Revenue tracking
- Restaurant count and average revenue metrics
- Channel-specific revenue (POS, Kiosk, Online)

### 📈 Analysis Modules

1. **Revenue Overview**
   - Revenue distribution by tier (Zero, 1K, 10K, 20K, 50K, 100K+)
   - Top 10 performing restaurants
   - Visual pie and bar charts

2. **Restaurant Analysis**
   - Individual restaurant performance comparison
   - Multi-restaurant selection and filtering
   - Stacked bar charts for channel revenue breakdown

3. **Channel Performance**
   - POS, Kiosk, and Online revenue distribution
   - Channel-specific metrics and comparisons
   - Performance metrics per channel

4. **Revenue Tiers**
   - Restaurant categorization by revenue brackets
   - Tier movement analysis across periods
   - Visual distribution of restaurants by tier

5. **Trends & Insights**
   - Statistical summaries (mean, median, std dev, IQR)
   - Revenue distribution histograms
   - Correlation analysis between metrics

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup
1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Make the run script executable:
```bash
chmod +x run_dashboard.sh
```

## Running the Dashboard

### Method 1: Using the launch script
```bash
./run_dashboard.sh
```

### Method 2: Direct Streamlit command
```bash
streamlit run restaurant_sales_dashboard.py
```

The dashboard will open automatically in your default browser at http://localhost:8501

## Data Requirements

The dashboard expects Excel files with the following columns:
- `Restaurant Name`: Name of the restaurant
- `Amount Collected`: Total revenue amount
- `POS Revenue%`: Percentage of revenue from POS
- `KIOSK Revenue%`: Percentage of revenue from Kiosk
- `ONLINE Revenue%`: Percentage of revenue from Online

### Supported Files
- Executive Sales Analytical Summary Excel files (.xlsx)
- Multiple file upload supported for period comparisons

## Usage

1. **Upload Data**: Use the sidebar file uploader to load Excel files
2. **Configure Tiers**: Adjust revenue tier thresholds in the sidebar
3. **Explore Tabs**: Navigate through different analysis modules
4. **Filter Data**: Use interactive filters to focus on specific restaurants
5. **Export Results**: Download processed data as Excel or CSV

## Key Improvements Over Original Notebook

- **Interactive Web Interface**: No coding required for analysis
- **Enhanced Visualizations**: Plotly charts with hover details and zoom
- **Real-time Filtering**: Dynamic restaurant and metric selection
- **Multiple Period Support**: Compare data across different time periods
- **Export Functionality**: Download processed data and insights
- **Responsive Design**: Works on desktop and mobile browsers
- **Revenue Tier Configuration**: Adjustable tier thresholds
- **Statistical Analysis**: Built-in correlation and distribution analysis

## Customization

### Modifying Revenue Tiers
Adjust the tier values in the sidebar configuration panel

### Adding New Metrics
Edit `restaurant_sales_dashboard.py` to add new calculated fields or visualizations

### Changing Color Schemes
Modify the `color_discrete_sequence` and `color_continuous_scale` parameters in the Plotly charts

## Troubleshooting

- **Port Already in Use**: Change port with `streamlit run restaurant_sales_dashboard.py --server.port 8502`
- **Memory Issues**: For large datasets, consider data sampling or aggregation
- **Missing Columns**: Ensure Excel files have required column names

## Support
For issues or enhancements, please check the data processing logic in the `process_dataframe()` function.