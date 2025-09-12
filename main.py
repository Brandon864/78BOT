#!/usr/bin/env python3
"""
Pocket Option AI Trading Bot (Lightweight Version)
A simple, efficient bot that analyzes OTC market conditions and places trades using a compounding strategy.
"""

import logging
import time
import sys
import signal
from datetime import datetime
from config import LOG_FILE, LOG_LEVEL

from technical_analysis import TechnicalAnalyzer
from human_behavior import HumanBehavior
from trading_strategy import TradingStrategy
from price_monitor import PriceMonitor

class PocketOptionBot:
    def __init__(self):
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.technical_analyzer = TechnicalAnalyzer()
        self.human_behavior = HumanBehavior()
        self.trading_strategy = TradingStrategy()
        self.price_monitor = PriceMonitor()
        
        self.is_running = False
        self.observation_complete = False
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=getattr(logging, LOG_LEVEL),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(LOG_FILE),
                logging.StreamHandler(sys.stdout)
            ]
        )
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.logger.info("Shutdown signal received. Stopping bot...")
        self.stop()
        sys.exit(0)
    
    def start(self):
        """Start the trading bot"""
        self.logger.info("=== Pocket Option AI Trading Bot Starting ===")
        self.logger.info("Version: Lightweight 1.0")
        self.logger.info("Strategy: Compounding with Technical Analysis")
        
        self.is_running = True
        
        # Start observation period
        self.start_observation_period()
        
        # Main trading loop
        self.main_trading_loop()
    
    def start_observation_period(self):
        """Start the 5-minute observation period"""
        self.logger.info("=== Starting Observation Period ===")
        self.price_monitor.start_observation_period()
        
        # Collect price data for 5 minutes
        start_time = time.time()
        while time.time() - start_time < 300:  # 5 minutes
            if not self.is_running:
                break
            
            self.price_monitor.collect_price_data()
            time.sleep(10)  # Collect data every 10 seconds
        
        # End observation period
        summary = self.price_monitor.end_observation_period()
        self.observation_complete = True
        
        self.logger.info("=== Observation Period Complete ===")
        self.logger.info(f"Collected {len(self.price_monitor.get_price_history())} price points")
    
    def main_trading_loop(self):
        """Main trading loop"""
        self.logger.info("=== Starting Main Trading Loop ===")
        
        while self.is_running:
            try:
                # Check if trading is allowed
                if not self.trading_strategy.can_trade():
                    self.logger.info("Trading not allowed. Waiting...")
                    time.sleep(60)  # Wait 1 minute
                    continue
                
                # Get current price data
                current_price = self.price_monitor.get_latest_price()
                if not current_price:
                    self.price_monitor.add_price_point(self.price_monitor.simulate_price_data())
                    current_price = self.price_monitor.get_latest_price()
                
                # Update price history
                self.price_monitor.add_price_point(current_price)
                price_history = self.price_monitor.get_price_history()
                
                # Perform technical analysis
                signal, signal_strength = self.technical_analyzer.analyze_all_indicators(price_history)
                
                # Check if we have a strong signal
                if signal != 0 and len(price_history) >= 20:
                    self.execute_trade(signal, signal_strength)
                else:
                    self.logger.info(f"No strong signal. Signal: {signal}, Strength: {signal_strength}")
                
                # Wait before next analysis
                time.sleep(30)  # Check every 30 seconds
                
            except KeyboardInterrupt:
                self.logger.info("Keyboard interrupt received")
                break
            except Exception as e:
                self.logger.error(f"Error in main trading loop: {e}")
                time.sleep(60)  # Wait before retrying
    
    def execute_trade(self, signal, signal_strength):
        """Execute a trade based on the signal"""
        try:
            # Determine trade direction
            direction = "CALL" if signal == 1 else "PUT"
            trade_amount = self.trading_strategy.get_trade_amount()
            
            self.logger.info(f"=== Executing Trade ===")
            self.logger.info(f"Direction: {direction}")
            self.logger.info(f"Amount: ${trade_amount}")
            self.logger.info(f"Signal Strength: {signal_strength}")
            
            # Set trade amount
            if not self.human_behavior.set_trade_amount(trade_amount):
                self.logger.error("Failed to set trade amount")
                return
            
            # Place trade
            trade_success = False
            if direction == "CALL":
                trade_success = self.human_behavior.place_call_trade()
            else:
                trade_success = self.human_behavior.place_put_trade()
            
            if not trade_success:
                self.logger.error("Failed to place trade")
                return
            
            # Wait for trade result
            result = self.human_behavior.wait_for_trade_result()
            
            # Update strategy based on result
            if result == "WIN":
                self.trading_strategy.update_after_win()
            else:
                self.trading_strategy.update_after_loss()
            
            # Log trade
            self.trading_strategy.log_trade(direction, trade_amount, signal_strength, result)
            
            # Display current stats
            self.display_trading_stats()
            
        except Exception as e:
            self.logger.error(f"Error executing trade: {e}")
    
    def display_trading_stats(self):
        """Display current trading statistics"""
        stats = self.trading_strategy.get_trading_stats()
        
        self.logger.info("=== Trading Statistics ===")
        self.logger.info(f"Current Trade Amount: ${stats['current_trade_amount']:.2f}")
        self.logger.info(f"Estimated Balance: ${stats['estimated_balance']:.2f}")
        self.logger.info(f"Consecutive Losses: {stats['consecutive_losses']}")
        self.logger.info(f"Daily Wins: {stats['daily_wins']}/{stats['daily_wins']}")
        self.logger.info(f"Daily Losses: {stats['daily_losses']}/{stats['daily_losses']}")
        self.logger.info(f"In Cooldown: {stats['is_in_cooldown']}")
        self.logger.info(f"Can Trade: {stats['can_trade']}")
        self.logger.info("=" * 30)
    
    def stop(self):
        """Stop the trading bot"""
        self.logger.info("=== Stopping Trading Bot ===")
        self.is_running = False
        
        # Display final statistics
        self.display_trading_stats()
        
        self.logger.info("Bot stopped successfully")

def main():
    """Main entry point"""
    bot = PocketOptionBot()
    
    try:
        bot.start()
    except KeyboardInterrupt:
        bot.logger.info("Keyboard interrupt received")
    except Exception as e:
        bot.logger.error(f"Unexpected error: {e}")
    finally:
        bot.stop()

if __name__ == "__main__":
    main()