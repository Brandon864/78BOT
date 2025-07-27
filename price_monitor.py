import time
import random
import logging
from datetime import datetime, timedelta
from config import OBSERVATION_MINUTES

class PriceMonitor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.price_history = []
        self.observation_start_time = None
        self.is_observing = False
        
    def start_observation_period(self):
        """Start the 5-minute observation period"""
        self.observation_start_time = datetime.now()
        self.is_observing = True
        self.price_history = []
        
        self.logger.info(f"Starting {OBSERVATION_MINUTES} minute observation period...")
        self.logger.info("Collecting market data and establishing trends...")
    
    def simulate_price_data(self):
        """Simulate price data collection"""
        # Simulate realistic price movements
        if not self.price_history:
            base_price = random.uniform(1.2000, 1.3000)  # Simulate EUR/USD
        else:
            base_price = self.price_history[-1]
        
        # Add some volatility
        change = random.uniform(-0.0020, 0.0020)
        new_price = base_price + change
        
        # Ensure price stays within reasonable bounds
        new_price = max(1.1000, min(1.4000, new_price))
        
        return round(new_price, 4)
    
    def collect_price_data(self):
        """Collect price data during observation period"""
        if not self.is_observing:
            return
        
        price = self.simulate_price_data()
        timestamp = datetime.now()
        
        self.price_history.append(price)
        
        self.logger.debug(f"Price collected: {price} at {timestamp.strftime('%H:%M:%S')}")
        
        # Log significant price movements
        if len(self.price_history) > 1:
            change = price - self.price_history[-2]
            if abs(change) > 0.0010:
                direction = "UP" if change > 0 else "DOWN"
                self.logger.info(f"Significant price movement: {direction} {abs(change):.4f}")
    
    def analyze_market_trends(self):
        """Analyze market trends during observation"""
        if len(self.price_history) < 10:
            return "Insufficient data"
        
        # Calculate basic trend
        recent_prices = self.price_history[-10:]
        trend = "UP" if recent_prices[-1] > recent_prices[0] else "DOWN"
        
        # Calculate volatility
        price_changes = [abs(recent_prices[i] - recent_prices[i-1]) for i in range(1, len(recent_prices))]
        avg_volatility = sum(price_changes) / len(price_changes)
        
        # Identify support and resistance levels
        high = max(recent_prices)
        low = min(recent_prices)
        current = recent_prices[-1]
        
        # Determine market condition
        if current > (high + low) / 2:
            condition = "BULLISH"
        else:
            condition = "BEARISH"
        
        analysis = {
            'trend': trend,
            'volatility': round(avg_volatility, 4),
            'high': high,
            'low': low,
            'current': current,
            'condition': condition
        }
        
        self.logger.info(f"Market Analysis: {analysis}")
        return analysis
    
    def is_observation_complete(self):
        """Check if observation period is complete"""
        if not self.is_observing or not self.observation_start_time:
            return False
        
        elapsed_minutes = (datetime.now() - self.observation_start_time).total_seconds() / 60
        return elapsed_minutes >= OBSERVATION_MINUTES
    
    def get_observation_summary(self):
        """Get summary of observation period"""
        if not self.price_history:
            return "No price data collected"
        
        analysis = self.analyze_market_trends()
        
        summary = {
            'observation_duration': f"{OBSERVATION_MINUTES} minutes",
            'data_points_collected': len(self.price_history),
            'price_range': f"{min(self.price_history):.4f} - {max(self.price_history):.4f}",
            'current_price': self.price_history[-1],
            'market_analysis': analysis
        }
        
        self.logger.info(f"Observation Summary: {summary}")
        return summary
    
    def end_observation_period(self):
        """End the observation period"""
        if not self.is_observing:
            return
        
        self.is_observing = False
        summary = self.get_observation_summary()
        
        self.logger.info("Observation period completed!")
        self.logger.info(f"Ready to start trading with {len(self.price_history)} data points")
        
        return summary
    
    def get_price_history(self):
        """Get collected price history"""
        return self.price_history.copy()
    
    def get_latest_price(self):
        """Get the most recent price"""
        return self.price_history[-1] if self.price_history else None
    
    def add_price_point(self, price):
        """Add a new price point to history"""
        self.price_history.append(price)
        self.logger.debug(f"Added price point: {price}")
    
    def get_price_statistics(self):
        """Get basic price statistics"""
        if not self.price_history:
            return {}
        
        prices = self.price_history
        return {
            'count': len(prices),
            'min': min(prices),
            'max': max(prices),
            'current': prices[-1],
            'avg': sum(prices) / len(prices),
            'volatility': max(prices) - min(prices)
        }