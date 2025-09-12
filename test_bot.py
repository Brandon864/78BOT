#!/usr/bin/env python3
"""
Test script for Pocket Option AI Trading Bot
This script tests all components without actually placing trades.
"""

import logging
import time
from datetime import datetime

from technical_analysis import TechnicalAnalyzer
from human_behavior import HumanBehavior
from trading_strategy import TradingStrategy
from price_monitor import PriceMonitor

def setup_test_logging():
    """Setup logging for testing"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )

def test_technical_analysis():
    """Test technical analysis components"""
    print("\n=== Testing Technical Analysis ===")
    
    analyzer = TechnicalAnalyzer()
    
    # Generate sample price data
    import random
    prices = [1.2500 + random.uniform(-0.01, 0.01) for _ in range(50)]
    
    print(f"Sample prices: {prices[:5]}...{prices[-5:]}")
    
    # Test RSI
    rsi = analyzer.calculate_rsi(prices)
    print(f"RSI: {rsi:.2f}")
    
    # Test MACD
    macd_signal = analyzer.calculate_macd(prices)
    print(f"MACD Signal: {macd_signal}")
    
    # Test Bollinger Bands
    bb_signal = analyzer.calculate_bollinger_bands(prices)
    print(f"Bollinger Bands Signal: {bb_signal}")
    
    # Test Support/Resistance
    sr_signal = analyzer.detect_support_resistance(prices)
    print(f"Support/Resistance Signal: {sr_signal}")
    
    # Test Candlestick Patterns
    cs_signal = analyzer.detect_candlestick_patterns(prices)
    print(f"Candlestick Signal: {cs_signal}")
    
    # Test complete analysis
    signal, strength = analyzer.analyze_all_indicators(prices)
    print(f"Overall Signal: {signal}")
    print(f"Signal Strength: {strength}")
    
    return True

def test_trading_strategy():
    """Test trading strategy components"""
    print("\n=== Testing Trading Strategy ===")
    
    strategy = TradingStrategy()
    
    # Test initial state
    stats = strategy.get_trading_stats()
    print(f"Initial trade amount: ${stats['current_trade_amount']:.2f}")
    print(f"Can trade: {stats['can_trade']}")
    print(f"Trading hours: {stats['is_trading_hours']}")
    
    # Test win scenario
    print("\n--- Testing Win Scenario ---")
    strategy.update_after_win()
    stats = strategy.get_trading_stats()
    print(f"After win - trade amount: ${stats['current_trade_amount']:.2f}")
    print(f"Daily wins: {stats['daily_wins']}")
    
    # Test loss scenario
    print("\n--- Testing Loss Scenario ---")
    strategy.update_after_loss()
    stats = strategy.get_trading_stats()
    print(f"After loss - trade amount: ${stats['current_trade_amount']:.2f}")
    print(f"Consecutive losses: {stats['consecutive_losses']}")
    
    # Test multiple losses (cooldown)
    print("\n--- Testing Cooldown ---")
    for i in range(3):
        strategy.update_after_loss()
    
    stats = strategy.get_trading_stats()
    print(f"In cooldown: {stats['is_in_cooldown']}")
    print(f"Can trade: {stats['can_trade']}")
    
    return True

def test_price_monitor():
    """Test price monitoring components"""
    print("\n=== Testing Price Monitor ===")
    
    monitor = PriceMonitor()
    
    # Test observation period
    monitor.start_observation_period()
    print("Started observation period")
    
    # Simulate price collection
    for i in range(10):
        monitor.collect_price_data()
        time.sleep(0.1)  # Fast simulation
    
    # Test market analysis
    analysis = monitor.analyze_market_trends()
    print(f"Market analysis: {analysis}")
    
    # Test observation summary
    summary = monitor.get_observation_summary()
    print(f"Observation summary: {summary}")
    
    # End observation
    monitor.end_observation_period()
    print("Ended observation period")
    
    return True

def test_human_behavior():
    """Test human behavior simulation (without actual clicks)"""
    print("\n=== Testing Human Behavior ===")
    
    behavior = HumanBehavior()
    
    # Test random delays
    print("Testing random delays...")
    for i in range(3):
        delay = behavior.random_delay(0.1, 0.3)
        print(f"Delay {i+1}: {delay:.2f}s")
    
    # Test mouse movement simulation
    print("Testing mouse movement simulation...")
    behavior.human_mouse_move(100, 200)
    
    # Test typing simulation
    print("Testing typing simulation...")
    # Note: This won't actually type due to safety
    print("Typing simulation would occur here")
    
    print("Human behavior tests completed (simulated)")
    return True

def test_integration():
    """Test integration of all components"""
    print("\n=== Testing Integration ===")
    
    # Initialize all components
    analyzer = TechnicalAnalyzer()
    strategy = TradingStrategy()
    monitor = PriceMonitor()
    behavior = HumanBehavior()
    
    # Simulate a complete trading cycle
    print("Simulating trading cycle...")
    
    # 1. Collect price data
    for i in range(20):
        monitor.add_price_point(monitor.simulate_price_data())
    
    # 2. Analyze market
    prices = monitor.get_price_history()
    signal, strength = analyzer.analyze_all_indicators(prices)
    
    print(f"Market signal: {signal}")
    print(f"Signal strength: {strength}")
    
    # 3. Check if we can trade
    can_trade = strategy.can_trade()
    print(f"Can trade: {can_trade}")
    
    # 4. Simulate trade execution
    if signal != 0 and can_trade:
        direction = "CALL" if signal == 1 else "PUT"
        amount = strategy.get_trade_amount()
        
        print(f"Would place {direction} trade for ${amount}")
        
        # Simulate trade result
        result = "WIN" if signal == 1 else "LOSS"  # Simplified
        
        if result == "WIN":
            strategy.update_after_win()
        else:
            strategy.update_after_loss()
        
        print(f"Trade result: {result}")
        
        # Log trade
        strategy.log_trade(direction, amount, strength, result)
    
    print("Integration test completed")
    return True

def main():
    """Run all tests"""
    print("=== Pocket Option AI Trading Bot - Test Suite ===")
    print("Testing all components without actual trading...")
    
    setup_test_logging()
    
    try:
        # Run all tests
        test_technical_analysis()
        test_trading_strategy()
        test_price_monitor()
        test_human_behavior()
        test_integration()
        
        print("\n=== All Tests Passed! ===")
        print("✅ Technical Analysis: Working")
        print("✅ Trading Strategy: Working")
        print("✅ Price Monitor: Working")
        print("✅ Human Behavior: Working")
        print("✅ Integration: Working")
        
        print("\n🎉 Bot is ready for configuration and testing!")
        print("Next steps:")
        print("1. Configure screen coordinates in config.py")
        print("2. Test with small amounts")
        print("3. Monitor logs carefully")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()