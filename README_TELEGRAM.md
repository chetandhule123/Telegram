# NSE MACD Scanner with Telegram Alerts

## Features

✅ **Exact MACD Logic** - Uses your precise EMA and MACD calculations from Google Apps Script reference
✅ **Stock Data** - Monitors your exact list of 81 NSE stocks  
✅ **Bearish to Bullish Detection** - Focuses on signal transitions (SELL/WEAK SELL → BUY/WEAK BUY/STRONG BUY)
✅ **Telegram Integration** - Sends alerts with 45-minute cooldown using your exact logic
✅ **Real-time Scanning** - 4H and 1D timeframe analysis
✅ **IST Timezone** - All times in Indian Standard Time
✅ **Auto-refresh** - 15-minute scanning intervals
✅ **Modern UI** - Clean interface with progress tracking

## Telegram Setup

### Step 1: Create Telegram Bot
1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Choose a name and username for your bot
4. Copy the **BOT_TOKEN** you receive

### Step 2: Get Chat ID
1. Send any message to your new bot
2. Visit: `https://api.telegram.org/bot<BOT_TOKEN>/getUpdates`
3. Find your **CHAT_ID** in the response (number under "chat":{"id":...)

### Step 3: Configure Secrets
Update `.streamlit/secrets.toml`:
```toml
BOT_TOKEN = "your_actual_bot_token_here"
CHAT_ID = "your_actual_chat_id_here"
```

## Telegram Alert Features

- **Smart Cooldown**: 45-minute interval between Telegram messages (prevents spam)
- **Formatted Messages**: Clean markdown formatting with timeframes
- **TradingView Links**: Direct buttons to view charts for each detected stock
- **Symbol Extraction**: Clean symbol names (removes .NS suffix)
- **Batch Alerts**: Groups multiple signals in single message

## Files Included

- `app_simple_macd.py` - Main application with Telegram integration
- `app_macd_original.py` - Standalone version with your original logic
- `.streamlit/secrets.toml` - Telegram configuration template
- `.streamlit/config.toml` - Streamlit server configuration

## Signal Types

- **STRONG BUY**: MACD > Signal AND both positive
- **BUY**: MACD > Signal (general bullish)
- **WEAK BUY**: MACD > Signal but MACD negative (early bullish signal)
- **WEAK SELL**: MACD < Signal but MACD positive
- **SELL**: MACD < Signal (general bearish)
- **STRONG SELL**: MACD < Signal AND both negative

## Usage

1. Configure Telegram credentials in secrets.toml
2. Run: `streamlit run app_simple_macd.py`
3. Use "Scan Now" button or enable auto-refresh
4. Monitor Telegram for crossover alerts

## Cooldown Logic

- Telegram alerts only sent if 45+ minutes since last alert
- Prevents message flooding while ensuring important signals are delivered
- UI shows remaining cooldown time
- Balloons celebration still shows for immediate feedback

## Stock Universe

Monitors 81 carefully selected NSE stocks including major indices constituents and high-volume stocks across sectors like banking, IT, pharma, auto, metals, and energy.