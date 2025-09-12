import logging
import time
from datetime import datetime, time as dt_time
from config import (
    INITIAL_TRADE_AMOUNT, PROFIT_PERCENTAGE, MAX_CONSECUTIVE_LOSSES,
    COOLDOWN_MINUTES, DAILY_WIN_LIMIT, DAILY_LOSS_LIMIT,
    TRADING_START_TIME, TRADING_END_TIME, ACCOUNT_BALANCE_THRESHOLD
)

class TradingStrategy:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.current_trade_amount = INITIAL_TRADE_AMOUNT
        self.consecutive_losses = 0
        self.daily_wins = 0
        self.daily_losses = 0
        self.last_trade_time = None
        self.is_in_cooldown = False
        self.cooldown_start_time = None
        self.estimated_balance = 100.0  # Starting balance estimate
        
    def reset_daily_stats(self):
        """Reset daily statistics"""
        self.daily_wins = 0
        self.daily_losses = 0
        self.logger.info("Daily statistics reset")
    
    def is_trading_hours(self):
        """Check if current time is within trading hours"""
        current_time = datetime.now().time()
        return TRADING_START_TIME <= current_time <= TRADING_END_TIME
    
    def check_cooldown(self):
        """Check if bot is in cooldown period"""
        if not self.is_in_cooldown:
            return False
        
        if self.cooldown_start_time:
            elapsed_minutes = (datetime.now() - self.cooldown_start_time).total_seconds() / 60
            if elapsed_minutes >= COOLDOWN_MINUTES:
                self.is_in_cooldown = False
                self.cooldown_start_time = None
                self.logger.info("Cooldown period ended")
                return False
        
        return True
    
    def start_cooldown(self):
        """Start cooldown period after consecutive losses"""
        self.is_in_cooldown = True
        self.cooldown_start_time = datetime.now()
        self.logger.warning(f"Starting {COOLDOWN_MINUTES} minute cooldown after {MAX_CONSECUTIVE_LOSSES} consecutive losses")
    
    def can_trade(self):
        """Check if trading is allowed based on all conditions"""
        # Check trading hours
        if not self.is_trading_hours():
            self.logger.info("Outside trading hours")
            return False
        
        # Check cooldown
        if self.check_cooldown():
            self.logger.info("Bot is in cooldown period")
            return False
        
        # Check daily limits
        if self.daily_wins >= DAILY_WIN_LIMIT:
            self.logger.info(f"Daily win limit reached ({DAILY_WIN_LIMIT})")
            return False
        
        if self.daily_losses >= DAILY_LOSS_LIMIT:
            self.logger.info(f"Daily loss limit reached ({DAILY_LOSS_LIMIT})")
            return False
        
        # Check balance threshold
        if self.estimated_balance < ACCOUNT_BALANCE_THRESHOLD:
            self.logger.warning(f"Balance below threshold (${self.estimated_balance:.2f})")
            return False
        
        return True
    
    def get_trade_amount(self):
        """Get current trade amount based on compounding strategy"""
        return round(self.current_trade_amount, 2)
    
    def update_after_win(self):
        """Update strategy after a winning trade"""
        profit = self.current_trade_amount * PROFIT_PERCENTAGE
        self.current_trade_amount += profit
        self.consecutive_losses = 0
        self.daily_wins += 1
        self.estimated_balance += profit
        
        self.logger.info(f"WIN! Profit: ${profit:.2f}, Next trade amount: ${self.current_trade_amount:.2f}")
        self.logger.info(f"Daily wins: {self.daily_wins}/{DAILY_WIN_LIMIT}")
    
    def update_after_loss(self):
        """Update strategy after a losing trade"""
        self.current_trade_amount = INITIAL_TRADE_AMOUNT
        self.consecutive_losses += 1
        self.daily_losses += 1
        self.estimated_balance -= self.current_trade_amount
        
        self.logger.info(f"LOSS! Reset to initial amount: ${self.current_trade_amount:.2f}")
        self.logger.info(f"Consecutive losses: {self.consecutive_losses}/{MAX_CONSECUTIVE_LOSSES}")
        self.logger.info(f"Daily losses: {self.daily_losses}/{DAILY_LOSS_LIMIT}")
        
        # Check if cooldown should start
        if self.consecutive_losses >= MAX_CONSECUTIVE_LOSSES:
            self.start_cooldown()
    
    def get_trading_stats(self):
        """Get current trading statistics"""
        return {
            'current_trade_amount': self.current_trade_amount,
            'consecutive_losses': self.consecutive_losses,
            'daily_wins': self.daily_wins,
            'daily_losses': self.daily_losses,
            'estimated_balance': self.estimated_balance,
            'is_in_cooldown': self.is_in_cooldown,
            'can_trade': self.can_trade(),
            'is_trading_hours': self.is_trading_hours()
        }
    
    def log_trade(self, direction, amount, signal_strength, result):
        """Log trade details"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_entry = {
            'timestamp': timestamp,
            'direction': direction,
            'amount': amount,
            'signal_strength': signal_strength,
            'result': result,
            'estimated_balance': self.estimated_balance,
            'consecutive_losses': self.consecutive_losses,
            'daily_wins': self.daily_wins,
            'daily_losses': self.daily_losses
        }
        
        self.logger.info(f"TRADE LOG: {log_entry}")
        return log_entry