import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import time
from datetime import datetime, timedelta
import pytz
import requests
import os

# Page configuration
st.set_page_config(
    page_title="NSE MACD Scanner",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Get Telegram secrets (same as in reference file)
try:
    TELEGRAM_BOT_TOKEN = st.secrets["BOT_TOKEN"]
    TELEGRAM_CHAT_ID = st.secrets["CHAT_ID"]
except:
    # Fallback to environment variables if secrets not available
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    .alert-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border: 1px solid #e9ecef;
    }
    .status-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def get_ist_time():
    """Get current IST time"""
    ist = pytz.timezone('Asia/Kolkata')
    return datetime.now(ist)

# Stock symbols - EXACT SAME as user provided
STOCK_SYMBOLS = [
    "ADANIENT.NS", "ADANIPORTS.NS", "APOLLOHOSP.NS", "ASIANPAINT.NS", "AXISBANK.NS",
    "BAJAJ-AUTO.NS", "BAJAJFINSV.NS", "BAJFINANCE.NS", "BHARTIARTL.NS", "BPCL.NS",
    "BRITANNIA.NS", "CIPLA.NS", "COALINDIA.NS", "DIVISLAB.NS", "DRREDDY.NS",
    "EICHERMOT.NS", "GRASIM.NS", "HCLTECH.NS", "HDFCBANK.NS", "HDFCLIFE.NS",
    "HEROMOTOCO.NS", "HINDALCO.NS", "HINDUNILVR.NS", "ICICIBANK.NS", "ICICIGI.NS",
    "ICICIPRULI.NS", "INDUSINDBK.NS", "INFY.NS", "ITC.NS", "JSWSTEEL.NS",
    "KOTAKBANK.NS", "LT.NS", "LTIM.NS", "M&M.NS", "MARUTI.NS",
    "NESTLEIND.NS", "NTPC.NS", "ONGC.NS", "POWERGRID.NS", "RELIANCE.NS",
    "SBILIFE.NS", "SBIN.NS", "SUNPHARMA.NS", "TATACONSUM.NS", "TATAMOTORS.NS",
    "TATASTEEL.NS", "TCS.NS", "TECHM.NS", "TITAN.NS", "ULTRACEMCO.NS",
    "UPL.NS", "WIPRO.NS", "DLF.NS", "SHRIRAMFIN.NS", "CHOLAFIN.NS",
    "BAJAJHLDNG.NS", "JINDALSTEL.NS", "RECLTD.NS", "ETERNAL.NS", "PFC.NS",
    "LODHA.NS", "SWIGGY.NS", "JIOFIN.NS", "ADANIPOWER.NS", "VBL.NS",
    "BANKBARODA.NS", "PNB.NS", "MOTHERSON.NS", "DMART.NS", "SIEMENS.NS",
    "TATAPOWER.NS", "JSWENERGY.NS", "ADANIGREEN.NS", "NAUKRI.NS", "ABB.NS",
    "TRENT.NS", "HAVELLS.NS", "IOC.NS", "SHREECEM.NS", "TVSMOTOR.NS",
    "AMBUJACEM.NS", "VEDL.NS", "BOSCHLTD.NS", "INDHOTEL.NS",
    "GAIL.NS", "GODREJCP.NS", "IRFC.NS", "ZYDUSLIFE.NS",
    "CANBK.NS", "BEL.NS", "DABUR.NS", "HAL.NS", "CGPOWER.NS"
]

# Initialize session state
if 'scan_interval' not in st.session_state:
    st.session_state.scan_interval = 15

if 'last_scan_time' not in st.session_state:
    st.session_state.last_scan_time = get_ist_time() - timedelta(minutes=st.session_state.scan_interval + 1)

if 'crossover_data_4h' not in st.session_state:
    st.session_state.crossover_data_4h = []
    
if 'crossover_data_1d' not in st.session_state:
    st.session_state.crossover_data_1d = []
    
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = False
    
if 'previous_alerts' not in st.session_state:
    st.session_state.previous_alerts = set()

if 'notification_enabled' not in st.session_state:
    st.session_state.notification_enabled = True

if 'last_telegram_sent_time' not in st.session_state:
    st.session_state.last_telegram_sent_time = get_ist_time() - timedelta(minutes=46)

def format_time_12hr(dt):
    """Format datetime to 12-hour format"""
    return dt.strftime("%I:%M:%S %p")

def is_trading_hours():
    """Check if current time is within trading hours"""
    now = get_ist_time()
    return 0 <= now.hour < 24  # Allow 24/7 for demo

def calculate_ema(data, period):
    """Calculate Exponential Moving Average exactly like Google Apps Script"""
    if not data or len(data) == 0:
        return []
    
    k = 2 / (period + 1)
    ema_array = [data[0]]

    for i in range(1, len(data)):
        ema_value = data[i] * k + ema_array[i - 1] * (1 - k)
        ema_array.append(ema_value)

    return ema_array

def calculate_macd(close_prices):
    """Calculate MACD exactly like the Google Apps Script reference"""
    if len(close_prices) < 30:
        return None

    # Calculate EMAs using the exact same logic as Google Apps Script
    fast_ema = calculate_ema(close_prices, 12)
    slow_ema = calculate_ema(close_prices, 26)

    # MACD line
    macd_line = [fast_ema[i] - slow_ema[i] for i in range(len(fast_ema))]

    # Signal line (9-period EMA of MACD line)
    signal_line = calculate_ema(macd_line, 9)

    # Histogram (latest values)
    histogram = macd_line[-1] - signal_line[-1]

    # Generate signals using exact same logic as Google Apps Script
    signals = []
    for i in range(len(macd_line)):
        macd_val = macd_line[i]
        signal_val = signal_line[i]

        if macd_val > signal_val and macd_val > 0 and signal_val > 0:
            signals.append("STRONG BUY")
        elif macd_val < signal_val and macd_val < 0 and signal_val < 0:
            signals.append("STRONG SELL")
        elif macd_val > signal_val and macd_val < 0:
            signals.append("WEAK BUY")
        elif macd_val < signal_val and macd_val > 0:
            signals.append("WEAK SELL")
        elif macd_val > signal_val:
            signals.append("BUY")
        elif macd_val < signal_val:
            signals.append("SELL")
        else:
            signals.append("NO SIGNAL")

    return {
        'macd': macd_line[-1],
        'signal': signal_line[-1],
        'histogram': histogram,
        'signals': signals
    }

def scan_crossovers(timeframe='1d'):
    """Scan for MACD crossovers focusing on bearish to bullish transitions"""
    crossovers = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total_stocks = len(STOCK_SYMBOLS)

    for idx, symbol in enumerate(STOCK_SYMBOLS):
        try:
            progress = (idx + 1) / total_stocks
            progress_bar.progress(progress)
            status_text.text(f"Scanning {symbol.replace('.NS', '')} ({idx + 1}/{total_stocks})")
            
            stock = yf.Ticker(symbol)

            # Get data based on timeframe
            if timeframe == '4h':
                hist = stock.history(period="60d", interval="1h")
                if not hist.empty:
                    # Resample to 4-hour intervals
                    hist = hist.resample('4h').agg({
                        'Open': 'first',
                        'High': 'max',
                        'Low': 'min',
                        'Close': 'last',
                        'Volume': 'sum'
                    }).dropna()
            else:
                hist = stock.history(period="3mo", interval="1d")

            if hist.empty or len(hist) < 30:
                continue

            prices = hist['Close'].tolist()
            macd_data = calculate_macd(prices)

            if not macd_data:
                continue

            current_signal = macd_data['signals'][-1] if macd_data['signals'] else "NO SIGNAL"
            prev_signal = macd_data['signals'][-2] if len(macd_data['signals']) > 1 else "NO SIGNAL"

            # Focus on bearish to bullish transitions
            bearish_signals = ["SELL", "WEAK SELL", "STRONG SELL"]
            bullish_signals = ["BUY", "WEAK BUY", "STRONG BUY"]

            # Check for signal change from bearish to bullish
            if (prev_signal in bearish_signals and current_signal in bullish_signals):
                crossover_type = "bullish"

                crossovers.append({
                    'symbol': symbol.replace('.NS', ''),
                    'type': crossover_type,
                    'previous_type': prev_signal,
                    'current_signal': current_signal,
                    'timestamp': get_ist_time(),
                    'macd': macd_data['macd'],
                    'signal': macd_data['signal'],
                    'price': prices[-1],
                    'timeframe': timeframe
                })

            time.sleep(0.05)  # Reduced rate limiting

        except Exception as e:
            continue

    progress_bar.empty()
    status_text.empty()
    return crossovers

def send_telegram_alerts(alerts_4h, alerts_1d):
    """Send Telegram alerts exactly like in reference file"""
    bot_token = TELEGRAM_BOT_TOKEN
    chat_id = TELEGRAM_CHAT_ID

    if not bot_token or not chat_id:
        print("❌ Telegram credentials missing.")
        return

    # Extract and clean symbol strings from alert dicts
    def extract_symbols(alerts):
        return [a['symbol'].strip().upper() for a in alerts if 'symbol' in a and isinstance(a['symbol'], str)]

    alerts_4h_symbols = extract_symbols(alerts_4h)
    alerts_1d_symbols = extract_symbols(alerts_1d)

    # Prepare message
    message_lines = [
        "📈 *MACD Crossover Summary*",
        f"🕒 *Scanned at:* {get_ist_time().strftime('%d %b %Y, %I:%M %p')} IST\n"
    ]

    if alerts_4h_symbols:
        message_lines.append("⏱️ *4H Timeframe*")
        message_lines += [f"• {sym}" for sym in alerts_4h_symbols]
        message_lines.append("")

    if alerts_1d_symbols:
        message_lines.append("📅 *1D Timeframe*")
        message_lines += [f"• {sym}" for sym in alerts_1d_symbols]
        message_lines.append("")

    message_text = "\n".join(message_lines)

    # Build buttons (2 per row)
    inline_keyboard = []
    all_symbols = alerts_4h_symbols + alerts_1d_symbols
    row = []
    for i, sym in enumerate(all_symbols, 1):
        button = {
            "text": f"🔗 {sym}",
            "url": f"https://www.tradingview.com/chart/?symbol=NSE:{sym}"
        }
        row.append(button)
        if i % 2 == 0:
            inline_keyboard.append(row)
            row = []
    if row:
        inline_keyboard.append(row)

    payload = {
        "chat_id": chat_id,
        "text": message_text,
        "parse_mode": "Markdown",
        "reply_markup": {"inline_keyboard": inline_keyboard}
    }

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("✅ Telegram alert sent.")
            return True
        else:
            print("❌ Telegram error:", response.text)
            return False
    except Exception as e:
        print(f"❌ Telegram send failed: {e}")
        return False

def scan_stocks_now():
    """Perform a single scan of all stocks"""
    try:
        with st.spinner("Scanning stocks for bearish to bullish MACD crossovers..."):
            # Scan for 4H crossovers
            crossovers_4h = scan_crossovers('4h')

            # Scan for 1D crossovers
            crossovers_1d = scan_crossovers('1d')

            # Check for new alerts
            current_alerts_4h = {f"{c['symbol']}_{c['timestamp']}" for c in crossovers_4h}
            current_alerts_1d = {f"{c['symbol']}_{c['timestamp']}" for c in crossovers_1d}

            new_alerts_4h = [c for c in crossovers_4h if
                             f"{c['symbol']}_{c['timestamp']}" not in st.session_state.previous_alerts]
            new_alerts_1d = [c for c in crossovers_1d if
                             f"{c['symbol']}_{c['timestamp']}" not in st.session_state.previous_alerts]

            # Send notifications for new alerts
            all_new_alerts = new_alerts_4h + new_alerts_1d

            if all_new_alerts and st.session_state.notification_enabled:
                # Show celebration
                st.balloons()
                
                # Send Telegram only if 45 minutes have passed since last Telegram alert
                now = get_ist_time()
                time_since_last_telegram = (now - st.session_state.last_telegram_sent_time).total_seconds() / 60

                if time_since_last_telegram >= 45:
                    if send_telegram_alerts(new_alerts_4h, new_alerts_1d):
                        st.session_state.last_telegram_sent_time = now
                        st.success(f"📱 Telegram alert sent for {len(all_new_alerts)} new signals!")
                    else:
                        st.warning("📱 Telegram alert failed - check credentials")
                else:
                    st.info(f"⏱️ Telegram cooldown: {int(45 - time_since_last_telegram)} minutes remaining")

            # Update session state
            st.session_state.crossover_data_4h = crossovers_4h
            st.session_state.crossover_data_1d = crossovers_1d
            st.session_state.previous_alerts = current_alerts_4h | current_alerts_1d
            st.session_state.last_scan_time = get_ist_time()

            return len(crossovers_4h), len(crossovers_1d), len(all_new_alerts)

    except Exception as e:
        st.error(f"Scanner error: {str(e)}")
        return 0, 0, 0

def display_crossover_alerts(crossovers, timeframe):
    """Display crossover alerts with modern styling"""
    if not crossovers:
        st.markdown(f"""
        <div class="status-card">
            <h4>🔍 {timeframe} Scanner Active</h4>
            <p>Monitoring for bearish → bullish crossovers...</p>
        </div>
        """, unsafe_allow_html=True)
        return

    # Header with modern styling
    st.markdown(f"""
    <div class="alert-card">
        <h3>🚀 {timeframe} Bullish Breakouts ({len(crossovers)} alerts)</h3>
        <p>Stocks that switched from bearish to bullish signals</p>
    </div>
    """, unsafe_allow_html=True)

    for i, crossover in enumerate(crossovers):
        symbol = crossover['symbol']
        previous_type = crossover.get('previous_type', 'Unknown')
        current_signal = crossover.get('current_signal', 'Unknown')
        timestamp = crossover['timestamp']
        macd_value = crossover['macd']
        signal_value = crossover['signal']
        price = crossover.get('price', 'N/A')

        # Signal change indicator
        signal_change_text = f"{previous_type} → {current_signal}"

        # Create expandable container
        with st.expander(f"🔄 {symbol} - {signal_change_text} 📈", expanded=(i < 3)):
            # Metrics layout
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>Current Price</h4>
                    <h2 style="color: #28a745;">₹{price:.2f}</h2>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>MACD</h4>
                    <h2 style="color: #667eea;">{macd_value:.4f}</h2>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>Signal</h4>
                    <h2 style="color: #764ba2;">{signal_value:.4f}</h2>
                </div>
                """, unsafe_allow_html=True)

            with col4:
                time_display = format_time_12hr(timestamp) if isinstance(timestamp, datetime) else str(timestamp)
                st.markdown(f"""
                <div class="metric-card">
                    <h4>Time</h4>
                    <h2 style="color: #666;">{time_display}</h2>
                </div>
                """, unsafe_allow_html=True)

            # TradingView link
            tv_url = f"https://www.tradingview.com/chart/?symbol=NSE%3A{symbol}"
            st.markdown(f"[📊 View {timeframe.upper()} Chart on TradingView]({tv_url})")

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚀 NSE MACD Scanner</h1>
        <h3>AI-Powered Bearish → Bullish Crossover Detection</h3>
        <p>Advanced MACD analysis for Indian NSE stocks using your exact logic</p>
    </div>
    """, unsafe_allow_html=True)

    # Status dashboard
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        status_color = "#28a745" if st.session_state.auto_refresh else "#dc3545"
        status_text = "AUTO-SCAN ON" if st.session_state.auto_refresh else "MANUAL MODE"
        st.markdown(f"""
        <div class="metric-card">
            <h4>Scanner Status</h4>
            <h3 style="color: {status_color};">{status_text}</h3>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Monitoring</h4>
            <h3 style="color: #667eea;">{len(STOCK_SYMBOLS)} Stocks</h3>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        market_status = "OPEN" if is_trading_hours() else "CLOSED"
        market_color = "#28a745" if is_trading_hours() else "#dc3545"
        st.markdown(f"""
        <div class="metric-card">
            <h4>Market Status</h4>
            <h3 style="color: {market_color};">{market_status}</h3>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        last_scan = format_time_12hr(st.session_state.last_scan_time) if st.session_state.last_scan_time else "Never"
        st.markdown(f"""
        <div class="metric-card">
            <h4>Last Scan</h4>
            <h3 style="color: #764ba2;">{last_scan}</h3>
        </div>
        """, unsafe_allow_html=True)

    # Sidebar controls
    with st.sidebar:
        st.markdown("## 🎛️ Scanner Controls")

        # Scan button
        if st.button("🔍 Scan Now", use_container_width=True, type="primary"):
            count_4h, count_1d, total_count = scan_stocks_now()
            if total_count > 0:
                st.success(f"🎉 Found {total_count} bullish breakouts! ({count_4h} 4H, {count_1d} 1D)")
            else:
                st.info("Scan completed! No bearish-to-bullish crossovers found currently.")

        # Auto-refresh toggle
        st.session_state.auto_refresh = st.checkbox("🔄 Auto-refresh every 15 minutes", 
                                                    value=st.session_state.auto_refresh)

        # Notification settings
        st.session_state.notification_enabled = st.checkbox("📱 Telegram Alerts (45min cooldown)",
                                                            value=st.session_state.notification_enabled)

        # Show Telegram status
        if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
            st.success("✅ Telegram configured")
        else:
            st.error("❌ Telegram not configured")
            st.info("Add BOT_TOKEN and CHAT_ID to secrets")

        st.markdown("---")

        # Statistics
        st.markdown("### 📊 Statistics")
        total_4h = len(st.session_state.crossover_data_4h)
        total_1d = len(st.session_state.crossover_data_1d)

        st.metric("Total Active Alerts", f"{total_4h + total_1d}")
        st.metric("4H Timeframe", total_4h)
        st.metric("1D Timeframe", total_1d)

        # IST time
        ist_time = get_ist_time()
        st.markdown(f"**IST Time:** {format_time_12hr(ist_time)}")
        st.markdown("**Using your exact MACD logic**")

    # Main content
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("## 📈 4-Hour Timeframe")
        display_crossover_alerts(st.session_state.crossover_data_4h, "4H")

    with col2:
        st.markdown("## 📊 Daily Timeframe")
        display_crossover_alerts(st.session_state.crossover_data_1d, "1D")

    # Auto-refresh system
    if st.session_state.auto_refresh:
        current_time = get_ist_time()
        
        if st.session_state.last_scan_time is None:
            st.session_state.last_scan_time = current_time - timedelta(minutes=16)
        
        time_since_last_scan = (current_time - st.session_state.last_scan_time).total_seconds() / 60
        
        if time_since_last_scan >= 15:
            count_4h, count_1d, total_count = scan_stocks_now()
            if total_count > 0:
                st.success(f"🎉 Auto-scan detected {total_count} new bullish breakouts!")
            st.session_state.last_scan_time = current_time
        
        # Schedule next rerun
        time_until_next_scan = max(0, 15 * 60 - time_since_last_scan * 60)
        time.sleep(min(5, time_until_next_scan))
        st.rerun()

if __name__ == "__main__":
    main()