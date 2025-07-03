# NSE Stock Screener - Enhanced Technical Analysis Platform

## Overview

This is a comprehensive real-time NSE (National Stock Exchange) stock screener application built with Streamlit. The application provides automated technical analysis scanning capabilities for Indian stock markets, featuring multiple scanning strategies based on popular technical indicators.

## Features

### 🎯 Technical Scanners
- **MACD Scanner**: 15-minute intervals for momentum analysis
- **Range Breakout Scanner**: 4-hour intervals using Pine Script logic for range detection
- **Resistance Breakout Scanner**: 4-hour intervals for breakout + retracement detection
- **Support Level Scanner**: 4-hour intervals showing support & resistance levels

### 📊 Real-time Market Data
- Live market indices (NIFTY, BANKNIFTY, SENSEX, FINNIFTY, etc.)
- Real-time price updates during market hours
- Volume and change tracking

### ⚙️ Advanced Features
- **Automatic Scanning**: Configurable auto-scan intervals (5-60 minutes)
- **Filtering & Sorting**: Customizable result filtering and sorting options
- **Export Functionality**: Download scan results as CSV files
- **Risk-Reward Analysis**: Calculated ratios for better trading decisions
- **Market Sentiment**: Overall market sentiment analysis

## Installation

### Prerequisites
- Python 3.11+
- Required dependencies (automatically installed via requirements)

### Setup
1. Clone or download the project files
2. Install dependencies:
   ```bash
   pip install streamlit pandas numpy plotly yfinance
   ```
3. Run the application:
   ```bash
   streamlit run app.py
   ```

## Project Structure

```
nse_stock_screener/
├── app.py                          # Main Streamlit application
├── scanners/                       # Technical scanner modules
│   ├── macd_scanner.py             # MACD momentum scanner
│   ├── range_breakout_scanner.py   # Range detection & breakout scanner
│   ├── resistance_breakout_scanner.py  # Resistance level scanner
│   └── support_level_scanner.py    # Support/resistance analysis
├── utils/                          # Utility modules
│   ├── data_fetcher.py             # Yahoo Finance data integration
│   ├── market_indices.py           # Market indices tracking
│   └── technical_indicators.py     # Technical analysis calculations
├── .streamlit/                     # Streamlit configuration
│   └── config.toml                 # Server and theme settings
└── pyproject.toml                  # Project dependencies
```

## Usage

### Starting the Application
1. Run `streamlit run app.py`
2. Open your browser to `http://localhost:8501`

### Using the Scanners
1. **Configure Scanners**: Use the sidebar to enable/disable specific scanners
2. **Auto-Scan**: Enable automatic scanning with configurable intervals
3. **Manual Scan**: Click "Run Manual Scan" for immediate results
4. **Filter Results**: Use the sorting and filtering options in each scanner tab
5. **Export Data**: Download results as CSV files for further analysis

### Scanner Details

#### MACD Scanner (15-minute intervals)
- Detects bullish/bearish crossovers
- Identifies momentum changes
- Calculates signal strength based on histogram values

#### Range Breakout Scanner (4-hour intervals)
- Uses Pine Script-inspired range detection logic
- Identifies consolidation periods and breakouts
- Measures breakout strength and volume confirmation

#### Resistance Breakout Scanner (4-hour intervals)
- Identifies key resistance levels through multiple touches
- Detects fresh breakouts and retracement opportunities
- Flags failed breakouts for reversal trades

#### Support Level Scanner (4-hour intervals)
- Maps support and resistance zones
- Calculates risk-reward ratios
- Identifies optimal entry points near support

## Configuration

### Market Data
- **Data Source**: Yahoo Finance API
- **Stock Universe**: 100+ major NSE stocks
- **Update Frequency**: Real-time during market hours
- **Historical Data**: Up to 90 days lookback

### Technical Settings
- **MACD Parameters**: 12, 26, 9 (Fast, Slow, Signal)
- **ATR Length**: 500 periods for range detection
- **Support/Resistance**: Minimum 2-3 touches for confirmation
- **Tolerance Levels**: 2-3% for level matching

## Market Hours
- **NSE Trading Hours**: 9:15 AM to 3:30 PM IST (Monday-Friday)
- **Auto-detection**: Application automatically detects market status
- **After-hours**: Limited functionality with previous session data

## Data Export
- **Format**: CSV files with timestamp
- **Content**: Complete scanner results with all metrics
- **Download**: Direct browser download via Streamlit interface

## Technical Requirements
- **Memory**: Minimum 2GB RAM recommended
- **Network**: Stable internet connection for real-time data
- **Browser**: Modern web browser (Chrome, Firefox, Safari, Edge)

## Limitations
- **Rate Limiting**: Yahoo Finance API limits (handled automatically)
- **Stock Coverage**: Limited to major NSE stocks for performance
- **Historical Data**: Maximum 2 years of historical data available
- **Real-time Delay**: ~15-20 minute delay in data during market hours

## Troubleshooting

### Common Issues
1. **No Data Loading**: Check internet connection and Yahoo Finance availability
2. **Slow Performance**: Reduce number of stocks being scanned
3. **Memory Issues**: Restart the application periodically during heavy usage

### Error Messages
- **HTTP 404 Errors**: Some index symbols may be temporarily unavailable
- **Symbol Delisted**: Stocks removed from exchange (automatic handling)
- **Timeout Errors**: Network connectivity issues

## Disclaimer
- **Educational Use**: This tool is for educational and research purposes only
- **Investment Risk**: Past performance does not guarantee future results
- **Data Accuracy**: Market data provided by Yahoo Finance with inherent delays
- **Trading Decisions**: Users are responsible for their own investment decisions

## License
This project is for educational purposes. Please respect data source terms of service.

## Support
For issues and questions, refer to the project documentation or contact the development team.

---

**Last Updated**: July 2025
**Version**: 1.0.0
**Platform**: Streamlit Cloud Compatible