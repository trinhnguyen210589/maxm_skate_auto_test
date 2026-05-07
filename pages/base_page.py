"""
Base Page module for the MaxmAuto test framework.

Provides common methods and utilities for all page objects,
following the Page Object Model (POM) design pattern.
"""

from typing import Optional, Tuple
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    ElementNotInteractableException
)
from appium.webdriver.common.appiumby import AppiumBy
from config.config import Config
from utils.logger import get_logger
from utils.common import CommonUtils
from utils.screenshot import ScreenshotHelper


class BasePage:
    """
    Base class for all Page Objects in the test framework.
    
    This class provides common methods for interacting with mobile UI elements,
    including waiting for elements, clicking, sending keys, and checking visibility.
    All page classes should inherit from this base class.
    
    Attributes:
        driver: Appium WebDriver instance
        wait: WebDriverWait instance with default timeout
        logger: Logger instance for the page
        screenshot: ScreenshotHelper instance for capturing screenshots
    """
    
    # Page-specific locators should be defined in subclasses
    PAGE_TITLE = None
    PAGE_URL = None
    
    def __init__(self, driver):
        """
        Initialize BasePage with a WebDriver instance.
        
        Args:
            driver: Appium WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT_MEDIUM)
        self.logger = get_logger(self.__class__.__name__)
        self.screenshot = ScreenshotHelper(driver)
    
    # ==================== WAIT METHODS ====================
    
    def wait_for_element(self, by, value, timeout=None, raise_exc=False):
        """
        Wait for an element to be present in the DOM.
        
        Args:
            by: Locator strategy (AppiumBy)
            value: Locator value
            timeout: Maximum time to wait (in seconds). If None, uses default.
            raise_exc: If True, raise TimeoutException on failure
            
        Returns:
            WebElement if found, None otherwise
            
        Raises:
            TimeoutException: If raise_exc is True and element not found
        """
        timeout = timeout or Config.EXPLICIT_WAIT_MEDIUM
        try:
            self.logger.debug(f"Waiting for element: {by}={value}")
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            self.logger.debug(f"✅ Element found: {by}={value}")
            return element
        except TimeoutException:
            self.logger.warning(f"⏰ Timeout waiting for element: {by}={value}")
            if raise_exc:
                raise
            return None
    
    def wait_for_element_visible(self, by, value, timeout=None, raise_exc=False):
        """
        Wait for an element to be visible on the screen.
        
        Args:
            by: Locator strategy (AppiumBy)
            value: Locator value
            timeout: Maximum time to wait (in seconds)
            raise_exc: If True, raise TimeoutException on failure
            
        Returns:
            WebElement if visible, None otherwise
            
        Raises:
            TimeoutException: If raise_exc is True and element not visible
        """
        timeout = timeout or Config.EXPLICIT_WAIT_MEDIUM
        try:
            self.logger.debug(f"Waiting for visible element: {by}={value}")
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
            self.logger.debug(f"✅ Element visible: {by}={value}")
            return element
        except TimeoutException:
            self.logger.warning(f"⏰ Timeout waiting for visible element: {by}={value}")
            if raise_exc:
                raise
            return None
    
    def wait_for_element_clickable(self, by, value, timeout=None, raise_exc=False):
        """
        Wait for an element to be clickable.
        
        Args:
            by: Locator strategy (AppiumBy)
            value: Locator value
            timeout: Maximum time to wait (in seconds)
            raise_exc: If True, raise TimeoutException on failure
            
        Returns:
            WebElement if clickable, None otherwise
            
        Raises:
            TimeoutException: If raise_exc is True and element not clickable
        """
        timeout = timeout or Config.EXPLICIT_WAIT_MEDIUM
        try:
            self.logger.debug(f"Waiting for clickable element: {by}={value}")
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            self.logger.debug(f"✅ Element clickable: {by}={value}")
            return element
        except TimeoutException:
            self.logger.warning(f"⏰ Timeout waiting for clickable element: {by}={value}")
            if raise_exc:
                raise
            return None
    
    def wait_for_element_gone(self, by, value, timeout=None):
        """
        Wait for an element to disappear from the screen.
        
        Args:
            by: Locator strategy (AppiumBy)
            value: Locator value
            timeout: Maximum time to wait (in seconds)
            
        Returns:
            bool: True if element is gone, False if timeout
        """
        timeout = timeout or Config.EXPLICIT_WAIT_MEDIUM
        try:
            self.logger.debug(f"Waiting for element to disappear: {by}={value}")
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located((by, value))
            )
            self.logger.debug(f"✅ Element disappeared: {by}={value}")
            return True
        except TimeoutException:
            self.logger.warning(f"⏰ Timeout waiting for element to disappear: {by}={value}")
            return False
    
    def wait_for_text(self, by, value, text, timeout=None, raise_exc=False):
        """
        Wait for an element to contain specific text.
        
        Args:
            by: Locator strategy (AppiumBy)
            value: Locator value
            text: Expected text content
            timeout: Maximum time to wait (in seconds)
            raise_exc: If True, raise TimeoutException on failure
            
        Returns:
            WebElement if text found, None otherwise
            
        Raises:
            TimeoutException: If raise_exc is True and text not found
        """
        timeout = timeout or Config.EXPLICIT_WAIT_MEDIUM
        try:
            self.logger.debug(f"Waiting for text '{text}' in element: {by}={value}")
            element = WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element((by, value), text)
            )
            self.logger.debug(f"✅ Text found: '{text}' in {by}={value}")
            return element
        except TimeoutException:
            self.logger.warning(f"⏰ Timeout waiting for text '{text}' in element: {by}={value}")
            if raise_exc:
                raise
            return None
    
    # ==================== FIND METHODS ====================
    
    def find_element(self, by, value):
        """
        Find an element on the page.
        
        Args:
            by: Locator strategy (AppiumBy)
            value: Locator value
            
        Returns:
            WebElement if found, None otherwise
        """
        try:
            return self.driver.find_element(by, value)
        except NoSuchElementException:
            self.logger.debug(f"Element not found: {by}={value}")
            return None
        except Exception as e:
            self.logger.error(f"Error finding element {by}={value}: {e}")
            return None
    
    def find_elements(self, by, value):
        """
        Find all elements matching the locator.
        
        Args:
            by: Locator strategy (AppiumBy)
            value: Locator value
            
        Returns:
            List of WebElements, or empty list if none found
        """
        try:
            return self.driver.find_elements(by, value)
        except Exception as e:
            self.logger.error(f"Error finding elements {by}={value}: {e}")
            return []
    
    # ==================== CLICK METHODS ====================
    
    def click(self, by, value, timeout=None, force=False):
        """
        Click on an element.
        
        Args:
            by: Locator strategy (AppiumBy)
            value: Locator value
            timeout: Maximum time to wait for element to be clickable
            force: If True, use force tap when normal click fails
            
        Returns:
            bool: True if click successful, False otherwise
        """
        try:
            element = self.wait_for_element_clickable(by, value, timeout)
            if element:
                element.click()
                self.logger.debug(f"✅ Clicked: {by}={value}")
                return True
            return False
        except (StaleElementReferenceException, ElementNotInteractableException) as e:
            self.logger.warning(f"Normal click failed, retrying: {e}")
            if force:
                return self.force_click(by, value)
            return False
        except Exception as e:
            self.logger.error(f"❌ Click failed: {by}={value}, Error: {e}")
            if force:
                return self.force_click(by, value)
            return False
    
    def force_click(self, by, value):
        """
        Force click on an element using coordinates.
        
        Args:
            by: Locator strategy (AppiumBy)
            value: Locator value
            
        Returns:
            bool: True if force click successful, False otherwise
        """
        try:
            element = self.find_element(by, value)
            if element:
                location = element.location
                size = element.size
                
                # Calculate center of element
                x = location['x'] + size['width'] / 2
                y = location['y'] + size['height'] / 2
                
                # Convert to percentage
                screen_size = self.driver.get_window_size()
                x_percent = x / screen_size['width']
                y_percent = y / screen_size['height']
                
                self.logger.debug(f"Force clicking at percentage: ({x_percent}, {y_percent})")
                return CommonUtils.force_tap(self.driver, x_percent, y_percent)
            return False
        except Exception as e:
            self.logger.error(f"❌ Force click failed: {by}={value}, Error: {e}")
            return False
    
    # ==================== INPUT METHODS ====================
    
    def send_keys(self, by, value, text, clear_first=True):
        """
        Send keys to an input element.
        
        Args:
            by: Locator strategy (AppiumBy)
            value: Locator value
            text: Text to send
            clear_first: If True, clear existing text first
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            element = self.wait_for_element_clickable(by, value)
            if element:
                if clear_first:
                    element.clear()
                element.send_keys(text)
                self.logger.debug(f"✅ Sent keys to {by}={value}: '{text}'")
                return True
            return False
        except Exception as e:
            self.logger.error(f"❌ Send keys failed: {by}={value}, Error: {e}")
            return False
    
    def clear_field(self, by, value):
        """
        Clear an input field.
        
        Args:
            by: Locator strategy (AppiumBy)
            value: Locator value
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            element = self.find_element(by, value)
            if element:
                element.clear()
                self.logger.debug(f"✅ Cleared field: {by}={value}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"❌ Clear field failed: {by}={value}, Error: {e}")
            return False
    
    # ==================== VISIBILITY CHECKS ====================
    
    def is_displayed(self, by, value, timeout=None):
        """
        Check if an element is displayed on the screen.
        
        Args:
            by: Locator strategy (AppiumBy)
            value: Locator value
            timeout: Maximum time to wait (in seconds)
            
        Returns:
            bool: True if element is displayed, False otherwise
        """
        try:
            element = self.wait_for_element_visible(by, value, timeout or Config.EXPLICIT_WAIT_SHORT)
            if element:
                return element.is_displayed()
            return False
        except Exception as e:
            self.logger.debug(f"Element not displayed: {by}={value}, Error: {e}")
            return False
    
    def is_present(self, by, value):
        """
        Check if an element is present in the DOM.
        
        Args:
            by: Locator strategy (AppiumBy)
            value: Locator value
            
        Returns:
            bool: True if element is present, False otherwise
        """
        try:
            element = self.find_element(by, value)
            return element is not None
        except NoSuchElementException:
            return False
    
    def get_text(self, by, value):
        """
        Get the text content of an element.
        
        Args:
            by: Locator strategy (AppiumBy)
            value: Locator value
            
        Returns:
            str: Text content, or empty string if not found
        """
        try:
            element = self.find_element(by, value)
            if element:
                return element.text
            return ""
        except Exception as e:
            self.logger.error(f"❌ Get text failed: {by}={value}, Error: {e}")
            return ""
    
    def get_attribute(self, by, value, attribute):
        """
        Get an attribute value of an element.
        
        Args:
            by: Locator strategy (AppiumBy)
            value: Locator value
            attribute: Attribute name
            
        Returns:
            str: Attribute value, or None if not found
        """
        try:
            element = self.find_element(by, value)
            if element:
                return element.get_attribute(attribute)
            return None
        except Exception as e:
            self.logger.error(f"❌ Get attribute failed: {by}={value}, Error: {e}")
            return None
    
    # ==================== NAVIGATION & SCREEN ====================
    
    def swipe_up(self):
        """
        Perform an upward swipe gesture.
        
        Returns:
            bool: True if swipe successful
        """
        return CommonUtils.swipe_up(self.driver)
    
    def swipe_down(self):
        """
        Perform a downward swipe gesture.
        
        Returns:
            bool: True if swipe successful
        """
        return CommonUtils.swipe_down(self.driver)
    
    def swipe_left(self):
        """
        Perform a left swipe gesture.
        
        Returns:
            bool: True if swipe successful
        """
        return CommonUtils.swipe_left(self.driver)
    
    def swipe_right(self):
        """
        Perform a right swipe gesture.
        
        Returns:
            bool: True if swipe successful
        """
        return CommonUtils.swipe_right(self.driver)
    
    def force_tap(self, x_percent, y_percent):
        """
        Perform a force tap at specified coordinates.
        
        Args:
            x_percent: X coordinate as percentage (0.0 to 1.0)
            y_percent: Y coordinate as percentage (0.0 to 1.0)
            
        Returns:
            bool: True if tap successful
        """
        return CommonUtils.force_tap(self.driver, x_percent, y_percent)
    
    def hide_keyboard(self):
        """
        Hide the soft keyboard if displayed.
        
        Returns:
            bool: True if keyboard was hidden
        """
        return CommonUtils.hide_keyboard(self.driver)
    
    def take_screenshot(self, name: str) -> str:
        """
        Take a screenshot and save it.
        
        Args:
            name: Base name for the screenshot file
            
        Returns:
            str: Path to the saved screenshot
        """
        return self.screenshot.capture(name)
    
    def is_keyboard_shown(self):
        """
        Check if the soft keyboard is displayed.
        
        Returns:
            bool: True if keyboard is shown
        """
        return self.driver.is_keyboard_shown()
    
    # ==================== PAGE VALIDATION ====================
    
    def is_page_loaded(self, timeout=None):
        """
        Check if the page is loaded.
        
        This method should be overridden in subclasses to provide
        page-specific validation logic.
        
        Args:
            timeout: Maximum time to wait (in seconds)
            
        Returns:
            bool: True if page is loaded
        """
        # Default implementation - override in subclasses
        self.logger.warning("is_page_loaded() not implemented for this page")
        return True