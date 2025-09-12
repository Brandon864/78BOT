#!/usr/bin/env python3
"""
Setup script for Pocket Option AI Trading Bot
"""

import os
import sys
import subprocess
import logging

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def create_env_file():
    """Create .env file with configuration"""
    env_content = """# Pocket Option AI Trading Bot Configuration
# Add your Pocket Option credentials here (optional)
POCKET_OPTION_USERNAME=your_username
POCKET_OPTION_PASSWORD=your_password

# Trading configuration
INITIAL_TRADE_AMOUNT=1.0
TRADING_HOURS_START=09:00
TRADING_HOURS_END=18:00

# Risk management
MAX_CONSECUTIVE_LOSSES=3
COOLDOWN_MINUTES=10
DAILY_WIN_LIMIT=10
DAILY_LOSS_LIMIT=5
"""
    
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Created .env file with default configuration")
    else:
        print("ℹ️  .env file already exists")

def check_screen_coordinates():
    """Check and update screen coordinates"""
    print("\n=== Screen Coordinate Setup ===")
    print("You need to configure the screen coordinates for your Pocket Option interface.")
    print("The bot will need to know where to click for:")
    print("- Login fields")
    print("- Trade amount field")
    print("- CALL/PUT buttons")
    print("- Chart area")
    
    print("\nTo get screen coordinates:")
    print("1. Open Pocket Option in your browser")
    print("2. Use a tool like 'xdotool' or 'xwininfo' to get coordinates")
    print("3. Update the SCREEN_COORDS in config.py")
    
    response = input("\nDo you want to update screen coordinates now? (y/n): ")
    if response.lower() == 'y':
        print("Please update the SCREEN_COORDS dictionary in config.py with your coordinates")
        print("Example format:")
        print("SCREEN_COORDS = {")
        print("    'login_button': (100, 200),")
        print("    'username_field': (100, 150),")
        print("    'password_field': (100, 180),")
        print("    'trade_amount_field': (300, 400),")
        print("    'call_button': (250, 500),")
        print("    'put_button': (350, 500),")
        print("    'chart_area': (100, 100, 800, 600),")
        print("}")

def create_directories():
    """Create necessary directories"""
    directories = ['logs', 'screenshots', 'data']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")

def main():
    """Main setup function"""
    print("=== Pocket Option AI Trading Bot Setup ===")
    print("This script will help you set up the trading bot.")
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Setup failed. Please check the error messages above.")
        return
    
    # Create directories
    create_directories()
    
    # Create .env file
    create_env_file()
    
    # Check screen coordinates
    check_screen_coordinates()
    
    print("\n=== Setup Complete ===")
    print("Next steps:")
    print("1. Update screen coordinates in config.py")
    print("2. Configure your trading parameters in config.py")
    print("3. Test the bot with: python main.py")
    print("4. Monitor logs in trading_log.txt")
    
    print("\n⚠️  IMPORTANT:")
    print("- This bot is for educational purposes")
    print("- Always test with small amounts first")
    print("- Monitor the bot while it's running")
    print("- Be aware of the risks involved in trading")

if __name__ == "__main__":
    main()