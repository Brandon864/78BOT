import pyautogui
import random
import time
import logging
from config import MIN_DELAY, MAX_DELAY, MOUSE_MOVEMENT_SPEED, SCREEN_COORDS

class HumanBehavior:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Set PyAutoGUI to fail-safe mode
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
        
    def random_delay(self, min_delay=None, max_delay=None):
        """Add random delay to simulate human behavior"""
        min_d = min_delay or MIN_DELAY
        max_d = max_delay or MAX_DELAY
        delay = random.uniform(min_d, max_d)
        time.sleep(delay)
        return delay
    
    def human_mouse_move(self, x, y, duration=None):
        """Move mouse in a human-like way with natural curves"""
        try:
            duration = duration or MOUSE_MOVEMENT_SPEED
            pyautogui.moveTo(x, y, duration=duration)
            self.logger.debug(f"Mouse moved to ({x}, {y})")
        except Exception as e:
            self.logger.error(f"Error moving mouse: {e}")
    
    def human_click(self, x, y, button='left'):
        """Click with human-like behavior"""
        try:
            # Move to position first
            self.human_mouse_move(x, y)
            self.random_delay(0.1, 0.3)
            
            # Click
            pyautogui.click(x, y, button=button)
            self.logger.debug(f"Clicked at ({x}, {y}) with {button} button")
            
            # Random delay after click
            self.random_delay(0.2, 0.5)
            
        except Exception as e:
            self.logger.error(f"Error clicking: {e}")
    
    def human_type(self, text, interval=0.05):
        """Type text with human-like intervals"""
        try:
            # Clear existing text first
            pyautogui.hotkey('ctrl', 'a')
            self.random_delay(0.1, 0.2)
            
            # Type with random intervals
            for char in text:
                pyautogui.typewrite(char)
                time.sleep(random.uniform(0.03, 0.08))
            
            self.logger.debug(f"Typed: {text}")
            
        except Exception as e:
            self.logger.error(f"Error typing: {e}")
    
    def login_to_pocket_option(self, username, password):
        """Simulate login to Pocket Option"""
        try:
            self.logger.info("Starting login process...")
            
            # Click username field
            self.human_click(*SCREEN_COORDS["username_field"])
            self.human_type(username)
            
            # Click password field
            self.human_click(*SCREEN_COORDS["password_field"])
            self.human_type(password)
            
            # Click login button
            self.human_click(*SCREEN_COORDS["login_button"])
            
            # Wait for login to complete
            self.random_delay(2, 4)
            
            self.logger.info("Login completed")
            return True
            
        except Exception as e:
            self.logger.error(f"Login failed: {e}")
            return False
    
    def set_trade_amount(self, amount):
        """Set the trade amount in the amount field"""
        try:
            self.logger.info(f"Setting trade amount to ${amount}")
            
            # Click amount field
            self.human_click(*SCREEN_COORDS["trade_amount_field"])
            
            # Clear and type new amount
            self.human_type(str(amount))
            
            # Press Enter to confirm
            pyautogui.press('enter')
            self.random_delay(0.5, 1.0)
            
            self.logger.info(f"Trade amount set to ${amount}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting trade amount: {e}")
            return False
    
    def place_call_trade(self):
        """Place a CALL trade"""
        try:
            self.logger.info("Placing CALL trade...")
            
            # Click CALL button
            self.human_click(*SCREEN_COORDS["call_button"])
            
            # Wait for trade to be placed
            self.random_delay(1, 2)
            
            self.logger.info("CALL trade placed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error placing CALL trade: {e}")
            return False
    
    def place_put_trade(self):
        """Place a PUT trade"""
        try:
            self.logger.info("Placing PUT trade...")
            
            # Click PUT button
            self.human_click(*SCREEN_COORDS["put_button"])
            
            # Wait for trade to be placed
            self.random_delay(1, 2)
            
            self.logger.info("PUT trade placed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error placing PUT trade: {e}")
            return False
    
    def take_screenshot(self, region=None):
        """Take a screenshot of the chart area"""
        try:
            if region is None:
                region = SCREEN_COORDS["chart_area"]
            
            screenshot = pyautogui.screenshot(region=region)
            return screenshot
            
        except Exception as e:
            self.logger.error(f"Error taking screenshot: {e}")
            return None
    
    def wait_for_trade_result(self, timeout=60):
        """Wait for trade result and return outcome"""
        try:
            self.logger.info("Waiting for trade result...")
            
            start_time = time.time()
            while time.time() - start_time < timeout:
                # Check for win/loss indicators on screen
                # This would need to be customized based on Pocket Option's UI
                
                # For now, we'll use a simple timeout
                time.sleep(1)
            
            # Default to random result for demo purposes
            # In real implementation, you'd analyze the screen for result
            result = random.choice(['WIN', 'LOSS'])
            self.logger.info(f"Trade result: {result}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error waiting for trade result: {e}")
            return 'LOSS'  # Default to loss on error
    
    def scroll_chart(self, direction='down', amount=100):
        """Scroll the chart to simulate human interaction"""
        try:
            if direction == 'down':
                pyautogui.scroll(-amount)
            else:
                pyautogui.scroll(amount)
            
            self.random_delay(0.5, 1.0)
            
        except Exception as e:
            self.logger.error(f"Error scrolling chart: {e}")
    
    def zoom_chart(self, direction='in'):
        """Zoom in/out on the chart"""
        try:
            if direction == 'in':
                pyautogui.hotkey('ctrl', 'plus')
            else:
                pyautogui.hotkey('ctrl', 'minus')
            
            self.random_delay(0.5, 1.0)
            
        except Exception as e:
            self.logger.error(f"Error zooming chart: {e}")