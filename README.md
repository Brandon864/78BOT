# Pocket Option AI Trading Bot (Lightweight Version)

A simple, efficient bot that analyzes OTC market conditions on Pocket Option, places trades using a compounding strategy, and mimics human actions without using the platform's API or GUI frameworks.

## 🚀 Features

### 💰 Compounding Trade Strategy
- Initial trade starts at $1
- On win: Add profit to next trade (e.g., $1 trade returns $0.92 profit → next trade = $1.92)
- On loss: Reset trade amount to $1

### 🕵️‍♂️ Pre-Trade Observation (5 mins)
- Bot waits and watches the market for the first 5 minutes after startup
- Collects and logs price action
- Detects early market trends
- Establishes support/resistance zones

### 📊 Technical Indicators
Uses 5 simple, yet powerful indicators:
- **RSI** (Relative Strength Index)
- **MACD** (Moving Average Convergence Divergence)
- **Bollinger Bands**
- **Support & Resistance** (basic detection via highs/lows)
- **Candlestick Patterns** (Engulfing, Doji)

Trade is only placed if at least 3 indicators agree on direction (CALL or PUT).

### 🤖 Human-like Behavior (No API)
- Uses PyAutoGUI to simulate mouse movement and clicks
- Types into fields (if login is needed)
- Introduces random delays between actions
- Mimics user interaction to avoid bot detection

### 📜 Trade Logging
- Prints or saves logs to a file
- Records time of trade, direction, signal strength, amount traded, result, and account balance estimate

### 🔐 Risk Management
- After 3 consecutive losses, pause for cooldown (10 minutes)
- Optional daily cap (stop after 10 wins or 5 losses)
- Only trade during predefined hours (9am–6pm)

## 📋 Requirements

- Python 3.7+
- Linux (tested on Ubuntu/Debian)
- X11 display server
- Pocket Option account

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd pocket-option-bot
   ```

2. **Run the setup script:**
   ```bash
   python setup.py
   ```

3. **Install dependencies manually (if needed):**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

### 1. Screen Coordinates
Update the `SCREEN_COORDS` in `config.py` with your Pocket Option interface coordinates:

```python
SCREEN_COORDS = {
    "login_button": (100, 200),
    "username_field": (100, 150),
    "password_field": (100, 180),
    "trade_amount_field": (300, 400),
    "call_button": (250, 500),
    "put_button": (350, 500),
    "chart_area": (100, 100, 800, 600),  # x, y, width, height
}
```

### 2. Trading Parameters
Modify trading parameters in `config.py`:

```python
# Trading Configuration
INITIAL_TRADE_AMOUNT = 1.0
PROFIT_PERCENTAGE = 0.92  # 92% return on win
MAX_CONSECUTIVE_LOSSES = 3
COOLDOWN_MINUTES = 10
DAILY_WIN_LIMIT = 10
DAILY_LOSS_LIMIT = 5

# Trading Hours (24-hour format)
TRADING_START_TIME = time(9, 0)  # 9:00 AM
TRADING_END_TIME = time(18, 0)   # 6:00 PM
```

## 🚀 Usage

### Quick Start
```bash
python main.py
```

### Running with Custom Configuration
```bash
# Set custom environment variables
export POCKET_OPTION_USERNAME="your_username"
export POCKET_OPTION_PASSWORD="your_password"
python main.py
```

## 📊 How It Works

### 1. Observation Period
- Bot starts with a 5-minute observation period
- Collects price data every 10 seconds
- Analyzes market trends and volatility
- Establishes support/resistance levels

### 2. Technical Analysis
- Continuously monitors price movements
- Calculates RSI, MACD, Bollinger Bands, Support/Resistance, and Candlestick patterns
- Only trades when at least 3 indicators agree on direction

### 3. Trade Execution
- Sets trade amount based on compounding strategy
- Simulates human-like mouse movements and clicks
- Waits for trade result
- Updates strategy based on win/loss

### 4. Risk Management
- Monitors consecutive losses
- Implements cooldown periods
- Respects daily win/loss limits
- Only trades during specified hours

## 📁 Project Structure

```
pocket-option-bot/
├── main.py                 # Main bot orchestrator
├── config.py              # Configuration settings
├── technical_analysis.py  # Technical indicators
├── human_behavior.py      # Human-like automation
├── trading_strategy.py    # Compounding strategy
├── price_monitor.py       # Price data collection
├── setup.py              # Installation script
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── trading_log.txt       # Trade logs (generated)
├── logs/                 # Log directory
├── screenshots/          # Screenshot directory
└── data/                 # Data directory
```

## 🔧 Customization

### Adding New Indicators
1. Add your indicator calculation in `technical_analysis.py`
2. Update the `analyze_all_indicators()` method
3. Modify signal strength requirements in `config.py`

### Changing Trading Strategy
1. Modify the compounding logic in `trading_strategy.py`
2. Update risk management parameters in `config.py`
3. Adjust trading hours and limits as needed

### Customizing Human Behavior
1. Update mouse movement patterns in `human_behavior.py`
2. Modify delays and timing in `config.py`
3. Add new interaction methods as needed

## ⚠️ Important Notes

### Legal and Risk Disclaimer
- This bot is for **educational purposes only**
- Trading involves significant risk of loss
- Always test with small amounts first
- Monitor the bot while it's running
- Be aware of your local trading regulations

### Technical Requirements
- Requires X11 display server (Linux)
- Screen coordinates must be accurately configured
- Pocket Option interface must be visible and accessible
- Stable internet connection required

### Limitations
- Bot detection: While the bot mimics human behavior, there's always a risk of detection
- Market conditions: No strategy works in all market conditions
- Technical issues: Screen resolution changes, interface updates, etc.

## 🐛 Troubleshooting

### Common Issues

1. **Screen coordinates not working**
   - Use `xdotool` to get accurate coordinates
   - Ensure Pocket Option is in the correct position
   - Test coordinates manually first

2. **Bot not placing trades**
   - Check if trading hours are correct
   - Verify screen coordinates
   - Check log files for errors

3. **Technical analysis not working**
   - Ensure sufficient price data is collected
   - Check indicator parameters in config
   - Verify data quality

### Debug Mode
Enable debug logging by changing `LOG_LEVEL` in `config.py`:
```python
LOG_LEVEL = "DEBUG"
```

## 📈 Performance Monitoring

### Log Files
- `trading_log.txt`: Detailed trade logs
- `logs/`: Additional log files
- Monitor for errors and performance issues

### Key Metrics
- Win rate
- Average trade amount
- Daily profit/loss
- Consecutive losses
- Account balance

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is for educational purposes. Use at your own risk.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review log files for errors
3. Test with small amounts first
4. Monitor bot behavior closely

---

**Remember: Trading involves risk. Only trade with money you can afford to lose.**
