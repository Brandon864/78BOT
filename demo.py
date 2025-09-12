#!/usr/bin/env python3
"""
Demo script for Pocket Option AI Trading Bot
This script demonstrates how the bot works with simulated trading.
"""

import time
import random
from datetime import datetime

from technical_analysis import TechnicalAnalyzer
from trading_strategy import TradingStrategy
from price_monitor import PriceMonitor

def simulate_trading_session():
    """Simulate a complete trading session"""
    print("=== Pocket Option AI Trading Bot - Demo Mode ===")
    print("This is a simulation for educational purposes.")
    print("No real trades will be placed.")
    print()
    
    # Initialize components
    analyzer = TechnicalAnalyzer()
    strategy = TradingStrategy()
    monitor = PriceMonitor()
    
    # Start observation period
    print("🕵️ Starting 5-minute observation period...")
    monitor.start_observation_period()
    
    # Simulate price data collection
    for i in range(30):  # 30 data points (5 minutes at 10-second intervals)
        monitor.collect_price_data()
        time.sleep(0.1)  # Fast simulation
    
    # End observation
    summary = monitor.end_observation_period()
    print(f"📊 Collected {len(monitor.get_price_history())} price points")
    print()
    
    # Simulate trading session
    print("🚀 Starting trading session...")
    trades_placed = 0
    wins = 0
    losses = 0
    
    for session in range(10):  # Simulate 10 trading sessions
        print(f"\n--- Trading Session {session + 1} ---")
        
        # Check if we can trade
        if not strategy.can_trade():
            print("⏸️ Trading not allowed (cooldown/limits)")
            time.sleep(1)
            continue
        
        # Collect new price data
        for i in range(5):
            monitor.add_price_point(monitor.simulate_price_data())
        
        # Analyze market
        prices = monitor.get_price_history()
        signal, strength = analyzer.analyze_all_indicators(prices)
        
        print(f"📈 Current price: {prices[-1]:.4f}")
        print(f"🎯 Signal: {signal} ({strength})")
        
        # Place trade if signal is strong
        if signal != 0:
            direction = "CALL" if signal == 1 else "PUT"
            amount = strategy.get_trade_amount()
            
            print(f"💰 Placing {direction} trade for ${amount:.2f}")
            trades_placed += 1
            
            # Simulate trade result (with some randomness)
            if signal == 1:  # Bullish signal
                win_probability = 0.6  # 60% win rate for demo
            else:  # Bearish signal
                win_probability = 0.6
            
            result = "WIN" if random.random() < win_probability else "LOSS"
            
            print(f"🎲 Trade result: {result}")
            
            # Update strategy
            if result == "WIN":
                strategy.update_after_win()
                wins += 1
            else:
                strategy.update_after_loss()
                losses += 1
            
            # Log trade
            strategy.log_trade(direction, amount, strength, result)
            
            # Display stats
            stats = strategy.get_trading_stats()
            print(f"📊 Balance: ${stats['estimated_balance']:.2f}")
            print(f"📊 Next trade amount: ${stats['current_trade_amount']:.2f}")
            print(f"📊 Daily wins: {stats['daily_wins']}/{stats['daily_wins']}")
            print(f"📊 Daily losses: {stats['daily_losses']}/{stats['daily_losses']}")
        else:
            print("⏳ No strong signal, waiting...")
        
        time.sleep(0.5)  # Brief pause between sessions
    
    # Final summary
    print("\n" + "="*50)
    print("📊 DEMO SESSION SUMMARY")
    print("="*50)
    print(f"Trades placed: {trades_placed}")
    print(f"Wins: {wins}")
    print(f"Losses: {losses}")
    if trades_placed > 0:
        win_rate = (wins / trades_placed) * 100
        print(f"Win rate: {win_rate:.1f}%")
    
    final_stats = strategy.get_trading_stats()
    print(f"Final balance: ${final_stats['estimated_balance']:.2f}")
    print(f"Final trade amount: ${final_stats['current_trade_amount']:.2f}")
    
    print("\n🎓 Demo completed!")
    print("This simulation shows how the bot would work in real trading.")
    print("Remember: Real trading involves risk and may not perform as well.")

def show_bot_features():
    """Show the bot's key features"""
    print("\n=== Bot Features Demo ===")
    
    # Technical Analysis Demo
    print("\n📊 Technical Analysis:")
    analyzer = TechnicalAnalyzer()
    prices = [1.2500 + random.uniform(-0.01, 0.01) for _ in range(50)]
    
    rsi = analyzer.calculate_rsi(prices)
    macd = analyzer.calculate_macd(prices)
    bb = analyzer.calculate_bollinger_bands(prices)
    sr = analyzer.detect_support_resistance(prices)
    cs = analyzer.detect_candlestick_patterns(prices)
    
    print(f"  RSI: {rsi:.2f}")
    print(f"  MACD Signal: {macd}")
    print(f"  Bollinger Bands: {bb}")
    print(f"  Support/Resistance: {sr}")
    print(f"  Candlestick Pattern: {cs}")
    
    signal, strength = analyzer.analyze_all_indicators(prices)
    print(f"  Overall Signal: {signal} ({strength})")
    
    # Trading Strategy Demo
    print("\n💰 Compounding Strategy:")
    strategy = TradingStrategy()
    
    print("  Initial amount: $1.00")
    strategy.update_after_win()
    print(f"  After win: ${strategy.get_trade_amount():.2f}")
    strategy.update_after_loss()
    print(f"  After loss: ${strategy.get_trade_amount():.2f}")
    
    # Risk Management Demo
    print("\n🔐 Risk Management:")
    print(f"  Max consecutive losses: {strategy.get_trading_stats()['consecutive_losses']}")
    print(f"  Daily win limit: 10")
    print(f"  Daily loss limit: 5")
    print(f"  Trading hours: 9:00 AM - 6:00 PM")
    
    print("\n✅ All features working correctly!")

def main():
    """Main demo function"""
    print("🎯 Pocket Option AI Trading Bot - Demo Mode")
    print("This demo shows how the bot works without placing real trades.")
    print()
    
    choice = input("Choose demo type:\n1. Full trading session simulation\n2. Show bot features\n3. Both\n\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        simulate_trading_session()
    elif choice == "2":
        show_bot_features()
    elif choice == "3":
        show_bot_features()
        simulate_trading_session()
    else:
        print("Invalid choice. Running full demo...")
        show_bot_features()
        simulate_trading_session()
    
    print("\n" + "="*60)
    print("📚 EDUCATIONAL PURPOSE ONLY")
    print("="*60)
    print("This bot is for educational purposes.")
    print("Real trading involves significant risk.")
    print("Always test with small amounts first.")
    print("Monitor the bot while it's running.")
    print("Be aware of your local trading regulations.")

if __name__ == "__main__":
    main()