"""
Common utilities module for the MaxmAuto test framework.

Provides helper functions for common operations like swipe gestures,
force tap, keyboard handling, and other utility functions.
"""

import time
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.action_chains import ActionChains
from config.config import Config
from utils.logger import get_logger


class CommonUtils:
    """
    Utility class providing common mobile automation helper methods.
    
    This class contains static methods for performing common actions
    like swipe gestures, force taps, and other utility operations.
    
    Example:
        >>> CommonUtils.swipe_up(driver)
        >>> CommonUtils.force_tap(driver, 0.5, 0.5)
    """
    
    _logger = get_logger(__name__)
    
    @staticmethod
    def swipe_up(driver, start_y_percent=None, end_y_percent=None, x_percent=None, duration=100):
        """
        Perform an upward swipe gesture on the screen.
        
        Args:
            driver: Appium WebDriver instance
            start_y_percent: Starting Y coordinate as percentage of screen height (default: 0.8)
            end_y_percent: Ending Y coordinate as percentage of screen height (default: 0.3)
            x_percent: X coordinate as percentage of screen width (default: 0.5)
            duration: Swipe duration in milliseconds (default: 100)
            
        Returns:
            bool: True if swipe was successful
        """
        try:
            start_y_percent = start_y_percent or Config.SWIPE_START_Y_PERCENT
            end_y_percent = end_y_percent or Config.SWIPE_END_Y_PERCENT
            x_percent = x_percent or Config.SWIPE_X_PERCENT
            
            size = driver.get_window_size()
            start_x = int(size['width'] * x_percent)
            start_y = int(size['height'] * start_y_percent)
            end_y = int(size['height'] * end_y_percent)
            
            CommonUtils._logger.debug(f"Swiping up from ({start_x}, {start_y}) to ({start_x}, {end_y})")
            
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(
                driver, 
                mouse=PointerInput(interaction.POINTER_TOUCH, "touch")
            )
            actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(duration / 1000)
            actions.w3c_actions.pointer_action.move_to_location(start_x, end_y)
            actions.w3c_actions.pointer_action.release()
            actions.perform()
            
            CommonUtils._logger.debug("✅ Swipe up completed")
            return True
            
        except Exception as e:
            CommonUtils._logger.error(f"❌ Swipe up failed: {e}")
            return False
    
    @staticmethod
    def swipe_down(driver, start_y_percent=None, end_y_percent=None, x_percent=None, duration=100):
        """
        Perform a downward swipe gesture on the screen.
        
        Args:
            driver: Appium WebDriver instance
            start_y_percent: Starting Y coordinate as percentage of screen height (default: 0.3)
            end_y_percent: Ending Y coordinate as percentage of screen height (default: 0.8)
            x_percent: X coordinate as percentage of screen width (default: 0.5)
            duration: Swipe duration in milliseconds (default: 100)
            
        Returns:
            bool: True if swipe was successful
        """
        try:
            start_y_percent = start_y_percent or Config.SWIPE_END_Y_PERCENT
            end_y_percent = end_y_percent or Config.SWIPE_START_Y_PERCENT
            x_percent = x_percent or Config.SWIPE_X_PERCENT
            
            size = driver.get_window_size()
            start_x = int(size['width'] * x_percent)
            start_y = int(size['height'] * start_y_percent)
            end_y = int(size['height'] * end_y_percent)
            
            CommonUtils._logger.debug(f"Swiping down from ({start_x}, {start_y}) to ({start_x}, {end_y})")
            
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(
                driver,
                mouse=PointerInput(interaction.POINTER_TOUCH, "touch")
            )
            actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(duration / 1000)
            actions.w3c_actions.pointer_action.move_to_location(start_x, end_y)
            actions.w3c_actions.pointer_action.release()
            actions.perform()
            
            CommonUtils._logger.debug("✅ Swipe down completed")
            return True
            
        except Exception as e:
            CommonUtils._logger.error(f"❌ Swipe down failed: {e}")
            return False
    
    @staticmethod
    def swipe_left(driver, start_x_percent=0.8, end_x_percent=0.2, y_percent=0.5, duration=100):
        """
        Perform a left swipe gesture on the screen.
        
        Args:
            driver: Appium WebDriver instance
            start_x_percent: Starting X coordinate as percentage of screen width
            end_x_percent: Ending X coordinate as percentage of screen width
            y_percent: Y coordinate as percentage of screen height
            duration: Swipe duration in milliseconds
            
        Returns:
            bool: True if swipe was successful
        """
        try:
            size = driver.get_window_size()
            start_x = int(size['width'] * start_x_percent)
            start_y = int(size['height'] * y_percent)
            end_x = int(size['width'] * end_x_percent)
            
            CommonUtils._logger.debug(f"Swiping left from ({start_x}, {start_y}) to ({end_x}, {start_y})")
            
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(
                driver,
                mouse=PointerInput(interaction.POINTER_TOUCH, "touch")
            )
            actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(duration / 1000)
            actions.w3c_actions.pointer_action.move_to_location(end_x, start_y)
            actions.w3c_actions.pointer_action.release()
            actions.perform()
            
            CommonUtils._logger.debug("✅ Swipe left completed")
            return True
            
        except Exception as e:
            CommonUtils._logger.error(f"❌ Swipe left failed: {e}")
            return False
    
    @staticmethod
    def swipe_right(driver, start_x_percent=0.2, end_x_percent=0.8, y_percent=0.5, duration=100):
        """
        Perform a right swipe gesture on the screen.
        
        Args:
            driver: Appium WebDriver instance
            start_x_percent: Starting X coordinate as percentage of screen width
            end_x_percent: Ending X coordinate as percentage of screen width
            y_percent: Y coordinate as percentage of screen height
            duration: Swipe duration in milliseconds
            
        Returns:
            bool: True if swipe was successful
        """
        try:
            size = driver.get_window_size()
            start_x = int(size['width'] * start_x_percent)
            start_y = int(size['height'] * y_percent)
            end_x = int(size['width'] * end_x_percent)
            
            CommonUtils._logger.debug(f"Swiping right from ({start_x}, {start_y}) to ({end_x}, {start_y})")
            
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(
                driver,
                mouse=PointerInput(interaction.POINTER_TOUCH, "touch")
            )
            actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(duration / 1000)
            actions.w3c_actions.pointer_action.move_to_location(end_x, start_y)
            actions.w3c_actions.pointer_action.release()
            actions.perform()
            
            CommonUtils._logger.debug("✅ Swipe right completed")
            return True
            
        except Exception as e:
            CommonUtils._logger.error(f"❌ Swipe right failed: {e}")
            return False
    
    @staticmethod
    def force_tap(driver, x_percent, y_percent):
        """
        Perform a force tap at specified screen coordinates.
        
        This method is useful when elements are not clickable through normal means
        or when precise coordinate-based tapping is needed.
        
        Args:
            driver: Appium WebDriver instance
            x_percent: X coordinate as percentage of screen width (0.0 to 1.0)
            y_percent: Y coordinate as percentage of screen height (0.0 to 1.0)
            
        Returns:
            bool: True if tap was successful
        """
        try:
            size = driver.get_window_size()
            x = int(size['width'] * x_percent)
            y = int(size['height'] * y_percent)
            
            CommonUtils._logger.debug(f"Force tapping at ({x_percent}, {y_percent}) -> ({x}, {y})")
            
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(
                driver,
                mouse=PointerInput(interaction.POINTER_TOUCH, "touch")
            )
            actions.w3c_actions.pointer_action.move_to_location(x, y)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()
            
            CommonUtils._logger.debug("✅ Force tap completed")
            return True
            
        except Exception as e:
            CommonUtils._logger.error(f"❌ Force tap failed: {e}")
            return False
    
    @staticmethod
    def hide_keyboard(driver):
        """
        Hide the soft keyboard if it's displayed.
        
        Args:
            driver: Appium WebDriver instance
            
        Returns:
            bool: True if keyboard was hidden, False if not displayed
        """
        try:
            if driver.is_keyboard_shown():
                driver.hide_keyboard()
                CommonUtils._logger.debug("✅ Keyboard hidden")
                return True
            return False
        except Exception as e:
            CommonUtils._logger.debug(f"Keyboard hide not needed or failed: {e}")
            return False
    
    @staticmethod
    def wait(seconds):
        """
        Static wait for specified number of seconds.
        
        Note: Use this sparingly. Prefer explicit waits with WebDriverWait.
        
        Args:
            seconds: Number of seconds to wait
        """
        CommonUtils._logger.debug(f"Waiting for {seconds} seconds...")
        time.sleep(seconds)
    
    @staticmethod
    def get_screen_size(driver):
        """
        Get the screen size of the device.
        
        Args:
            driver: Appium WebDriver instance
            
        Returns:
            dict: Dictionary containing 'width' and 'height'
        """
        return driver.get_window_size()
    
    @staticmethod
    def is_element_displayed(driver, by, value, timeout=5):
        """
        Check if an element is displayed on the screen.
        
        Args:
            driver: Appium WebDriver instance
            by: Locator strategy (AppiumBy)
            value: Locator value
            timeout: Maximum time to wait for element
            
        Returns:
            bool: True if element is displayed, False otherwise
        """
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.common.exceptions import TimeoutException
        
        try:
            wait = WebDriverWait(driver, timeout)
            element = wait.until(EC.visibility_of_element_located((by, value)))
            return element.is_displayed()
        except TimeoutException:
            return False
        except Exception as e:
            CommonUtils._logger.debug(f"Element check failed: {e}")
            return False