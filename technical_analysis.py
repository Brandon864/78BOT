import numpy as np
import pandas as pd
from ta.trend import MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands
import logging

class TechnicalAnalyzer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def calculate_rsi(self, prices, period=14):
        """Calculate RSI indicator"""
        try:
            rsi_indicator = RSIIndicator(close=pd.Series(prices), window=period)
            rsi = rsi_indicator.rsi()
            return rsi.iloc[-1] if not rsi.empty else 50
        except Exception as e:
            self.logger.error(f"Error calculating RSI: {e}")
            return 50
    
    def calculate_macd(self, prices, fast=12, slow=26, signal=9):
        """Calculate MACD indicator"""
        try:
            macd_indicator = MACD(close=pd.Series(prices), window_fast=fast, window_slow=slow, window_sign=signal)
            macd_line = macd_indicator.macd()
            signal_line = macd_indicator.macd_signal()
            
            if macd_line.empty or signal_line.empty:
                return 0
            
            # Return 1 for bullish, -1 for bearish, 0 for neutral
            if macd_line.iloc[-1] > signal_line.iloc[-1] and macd_line.iloc[-1] > 0:
                return 1
            elif macd_line.iloc[-1] < signal_line.iloc[-1] and macd_line.iloc[-1] < 0:
                return -1
            else:
                return 0
        except Exception as e:
            self.logger.error(f"Error calculating MACD: {e}")
            return 0
    
    def calculate_bollinger_bands(self, prices, period=20, std=2):
        """Calculate Bollinger Bands"""
        try:
            bb_indicator = BollingerBands(close=pd.Series(prices), window=period, window_dev=std)
            upper_band = bb_indicator.bollinger_hband()
            lower_band = bb_indicator.bollinger_lband()
            middle_band = bb_indicator.bollinger_mavg()
            
            if upper_band.empty or lower_band.empty or middle_band.empty:
                return 0
            
            current_price = prices[-1]
            upper = upper_band.iloc[-1]
            lower = lower_band.iloc[-1]
            middle = middle_band.iloc[-1]
            
            # Return 1 for bullish (price near lower band), -1 for bearish (price near upper band)
            if current_price <= lower + (upper - lower) * 0.2:
                return 1  # Bullish - price near lower band
            elif current_price >= upper - (upper - lower) * 0.2:
                return -1  # Bearish - price near upper band
            else:
                return 0  # Neutral
        except Exception as e:
            self.logger.error(f"Error calculating Bollinger Bands: {e}")
            return 0
    
    def detect_support_resistance(self, prices, window=10):
        """Detect basic support and resistance levels"""
        try:
            if len(prices) < window * 2:
                return 0
            
            recent_prices = prices[-window:]
            all_prices = prices[-window*2:]
            
            # Find local highs and lows
            highs = []
            lows = []
            
            for i in range(1, len(all_prices) - 1):
                if all_prices[i] > all_prices[i-1] and all_prices[i] > all_prices[i+1]:
                    highs.append(all_prices[i])
                elif all_prices[i] < all_prices[i-1] and all_prices[i] < all_prices[i+1]:
                    lows.append(all_prices[i])
            
            if not highs and not lows:
                return 0
            
            current_price = prices[-1]
            
            # Check if price is near resistance (highs)
            if highs:
                nearest_resistance = min(highs, key=lambda x: abs(x - current_price))
                if abs(current_price - nearest_resistance) / nearest_resistance < 0.02:  # Within 2%
                    return -1  # Bearish - near resistance
            
            # Check if price is near support (lows)
            if lows:
                nearest_support = min(lows, key=lambda x: abs(x - current_price))
                if abs(current_price - nearest_support) / nearest_support < 0.02:  # Within 2%
                    return 1  # Bullish - near support
            
            return 0
        except Exception as e:
            self.logger.error(f"Error detecting support/resistance: {e}")
            return 0
    
    def detect_candlestick_patterns(self, prices, volumes=None):
        """Detect basic candlestick patterns"""
        try:
            if len(prices) < 3:
                return 0
            
            # Simple pattern detection based on price movement
            current_price = prices[-1]
            prev_price = prices[-2]
            prev_prev_price = prices[-3]
            
            # Engulfing pattern detection
            if len(prices) >= 4:
                open1, close1 = prices[-4], prices[-3]  # Previous candle
                open2, close2 = prices[-2], prices[-1]  # Current candle
                
                # Bullish engulfing
                if close1 < open1 and close2 > open2 and close2 > open1 and open2 < close1:
                    return 1
                
                # Bearish engulfing
                elif close1 > open1 and close2 < open2 and close2 < open1 and open2 > close1:
                    return -1
            
            # Doji pattern (price stays relatively the same)
            if abs(current_price - prev_price) / prev_price < 0.001:  # Less than 0.1% change
                return 0  # Neutral - doji
            
            # Simple trend continuation
            if current_price > prev_price > prev_prev_price:
                return 1  # Bullish trend
            elif current_price < prev_price < prev_prev_price:
                return -1  # Bearish trend
            
            return 0
        except Exception as e:
            self.logger.error(f"Error detecting candlestick patterns: {e}")
            return 0
    
    def analyze_all_indicators(self, prices):
        """Analyze all technical indicators and return trading signal"""
        try:
            if len(prices) < 20:
                return 0, "Insufficient data"
            
            # Calculate all indicators
            rsi_value = self.calculate_rsi(prices)
            macd_signal = self.calculate_macd(prices)
            bb_signal = self.calculate_bollinger_bands(prices)
            sr_signal = self.detect_support_resistance(prices)
            candlestick_signal = self.detect_candlestick_patterns(prices)
            
            # Count bullish and bearish signals
            bullish_signals = 0
            bearish_signals = 0
            
            # RSI analysis
            if rsi_value < 30:
                bullish_signals += 1
            elif rsi_value > 70:
                bearish_signals += 1
            
            # MACD analysis
            if macd_signal == 1:
                bullish_signals += 1
            elif macd_signal == -1:
                bearish_signals += 1
            
            # Bollinger Bands analysis
            if bb_signal == 1:
                bullish_signals += 1
            elif bb_signal == -1:
                bearish_signals += 1
            
            # Support/Resistance analysis
            if sr_signal == 1:
                bullish_signals += 1
            elif sr_signal == -1:
                bearish_signals += 1
            
            # Candlestick analysis
            if candlestick_signal == 1:
                bullish_signals += 1
            elif candlestick_signal == -1:
                bearish_signals += 1
            
            # Determine final signal
            if bullish_signals >= 3:
                return 1, f"BULLISH - {bullish_signals} indicators agree"
            elif bearish_signals >= 3:
                return -1, f"BEARISH - {bearish_signals} indicators agree"
            else:
                return 0, f"NEUTRAL - Bullish: {bullish_signals}, Bearish: {bearish_signals}"
                
        except Exception as e:
            self.logger.error(f"Error in technical analysis: {e}")
            return 0, f"Error: {e}"