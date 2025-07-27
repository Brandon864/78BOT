#!/usr/bin/env python3
"""
Screen Coordinate Helper for Pocket Option AI Trading Bot
This script helps you get screen coordinates for your Pocket Option interface.
"""

import pyautogui
import time
import sys

def get_mouse_position():
    """Get current mouse position"""
    try:
        x, y = pyautogui.position()
        return x, y
    except Exception as e:
        print(f"Error getting mouse position: {e}")
        return None, None

def main():
    """Main coordinate helper function"""
    print("=== Pocket Option Screen Coordinate Helper ===")
    print("This tool will help you get screen coordinates for your Pocket Option interface.")
    print()
    print("Instructions:")
    print("1. Open Pocket Option in your browser")
    print("2. Make sure the interface is visible")
    print("3. Move your mouse to each element and press Enter")
    print("4. The coordinates will be displayed")
    print("5. Press Ctrl+C to exit")
    print()
    
    coordinates = {}
    
    try:
        while True:
            print("\nMove your mouse to the element and press Enter (or Ctrl+C to exit):")
            print("1. Username field")
            print("2. Password field") 
            print("3. Login button")
            print("4. Trade amount field")
            print("5. CALL button")
            print("6. PUT button")
            print("7. Chart area (top-left corner)")
            print("8. Chart area (bottom-right corner)")
            print("9. Show all coordinates")
            print("10. Generate config code")
            
            choice = input("\nEnter your choice (1-10): ").strip()
            
            if choice == "1":
                input("Move mouse to username field and press Enter...")
                x, y = get_mouse_position()
                if x is not None:
                    coordinates["username_field"] = (x, y)
                    print(f"Username field: ({x}, {y})")
            
            elif choice == "2":
                input("Move mouse to password field and press Enter...")
                x, y = get_mouse_position()
                if x is not None:
                    coordinates["password_field"] = (x, y)
                    print(f"Password field: ({x}, {y})")
            
            elif choice == "3":
                input("Move mouse to login button and press Enter...")
                x, y = get_mouse_position()
                if x is not None:
                    coordinates["login_button"] = (x, y)
                    print(f"Login button: ({x}, {y})")
            
            elif choice == "4":
                input("Move mouse to trade amount field and press Enter...")
                x, y = get_mouse_position()
                if x is not None:
                    coordinates["trade_amount_field"] = (x, y)
                    print(f"Trade amount field: ({x}, {y})")
            
            elif choice == "5":
                input("Move mouse to CALL button and press Enter...")
                x, y = get_mouse_position()
                if x is not None:
                    coordinates["call_button"] = (x, y)
                    print(f"CALL button: ({x}, {y})")
            
            elif choice == "6":
                input("Move mouse to PUT button and press Enter...")
                x, y = get_mouse_position()
                if x is not None:
                    coordinates["put_button"] = (x, y)
                    print(f"PUT button: ({x}, {y})")
            
            elif choice == "7":
                input("Move mouse to chart area top-left corner and press Enter...")
                x, y = get_mouse_position()
                if x is not None:
                    coordinates["chart_top_left"] = (x, y)
                    print(f"Chart top-left: ({x}, {y})")
            
            elif choice == "8":
                input("Move mouse to chart area bottom-right corner and press Enter...")
                x, y = get_mouse_position()
                if x is not None:
                    coordinates["chart_bottom_right"] = (x, y)
                    print(f"Chart bottom-right: ({x}, {y})")
            
            elif choice == "9":
                print("\n=== Current Coordinates ===")
                for name, coord in coordinates.items():
                    print(f"{name}: {coord}")
            
            elif choice == "10":
                generate_config_code(coordinates)
            
            else:
                print("Invalid choice. Please enter 1-10.")
    
    except KeyboardInterrupt:
        print("\n\nExiting coordinate helper...")
        if coordinates:
            print("\nFinal coordinates:")
            for name, coord in coordinates.items():
                print(f"{name}: {coord}")

def generate_config_code(coordinates):
    """Generate config.py code with the coordinates"""
    print("\n=== Generated Config Code ===")
    print("Copy this to your config.py file:")
    print()
    
    # Calculate chart area if we have both corners
    chart_area = None
    if "chart_top_left" in coordinates and "chart_bottom_right" in coordinates:
        x1, y1 = coordinates["chart_top_left"]
        x2, y2 = coordinates["chart_bottom_right"]
        width = x2 - x1
        height = y2 - y1
        chart_area = (x1, y1, width, height)
    
    print("SCREEN_COORDS = {")
    for name, coord in coordinates.items():
        if name.startswith("chart_"):
            continue
        print(f"    '{name}': {coord},")
    
    if chart_area:
        print(f"    'chart_area': {chart_area},  # x, y, width, height")
    
    print("}")
    print()
    print("Note: You may need to adjust these coordinates based on your screen resolution.")

if __name__ == "__main__":
    main()