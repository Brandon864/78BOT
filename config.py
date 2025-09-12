import os
from datetime import time

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

# Observation Period
OBSERVATION_MINUTES = 5

# Technical Analysis
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

BOLLINGER_PERIOD = 20
BOLLINGER_STD = 2

# Signal Strength
MIN_INDICATOR_AGREEMENT = 3  # At least 3 indicators must agree

# Human-like Behavior
MIN_DELAY = 0.5  # seconds
MAX_DELAY = 2.0  # seconds
MOUSE_MOVEMENT_SPEED = 0.5  # seconds

# Logging
LOG_FILE = "trading_log.txt"
LOG_LEVEL = "INFO"

# Screen Coordinates (to be calibrated)
# These will need to be adjusted based on your screen resolution
SCREEN_COORDS = {
    "login_button": (100, 200),
    "username_field": (100, 150),
    "password_field": (100, 180),
    "trade_amount_field": (300, 400),
    "call_button": (250, 500),
    "put_button": (350, 500),
    "chart_area": (100, 100, 800, 600),  # x, y, width, height
}

# Risk Management
ACCOUNT_BALANCE_THRESHOLD = 5.0  # Stop trading if balance falls below this