"""
Home Page Object for the MaxmAuto test framework.

Represents the home/main screen of the Maxm app and provides methods
for interacting with home screen UI elements.
"""

from appium.webdriver.common.appiumby import AppiumBy
from utils.logger import get_logger
from pages.base_page import BasePage


class HomePage(BasePage):
    """
    Page Object for the Home screen.
    
    This class represents the main home screen of the Maxm app that users
    see after successful login. It provides methods for verifying the home
    screen is loaded and interacting with home screen elements.
    
    Locators:
        - Various indicators to verify home screen is loaded
        - User profile name display
        - Session-related elements
        - Navigation elements
    """
    
    # ==================== PAGE LOCATORS ====================
    
    # Home screen indicators - any of these indicate we're on home screen
    HOME_INDICATORS = [
        # User profile/name display
        (AppiumBy.XPATH, "//android.widget.TextView[contains(@text, 'Trinh')]"),
        
        # Home navigation description
        (AppiumBy.XPATH, "//android.view.View[contains(@content-desc, 'Home')]"),
        
        # Session indicator
        (AppiumBy.XPATH, "//*[contains(@text, 'Session 1')]"),
        
        # Start session button
        (AppiumBy.XPATH, "//android.widget.Button"),
        
        # Home menu ID
        (AppiumBy.XPATH, "//*[@resource-id='Home']"),
    ]
    
    # Primary home screen verification element
    HOME_VERIFICATION = (AppiumBy.XPATH, "//*[contains(@text, 'Start Session 1')]")
    
    # Profile icon on home screen
    PROFILE_ICON = (AppiumBy.XPATH, "//android.widget.ImageView[@index='4']")
    
    def __init__(self, driver):
        """
        Initialize HomePage with a WebDriver instance.
        
        Args:
            driver: Appium WebDriver instance
        """
        super().__init__(driver)
        self.logger = get_logger(self.__class__.__name__)
    
    # ==================== PAGE VALIDATION ====================
    
    def is_page_loaded(self, timeout=None):
        """
        Check if the home page is loaded.
        
        Verifies that at least one of the home screen indicators is visible.
        
        Args:
            timeout: Maximum time to wait (in seconds)
            
        Returns:
            bool: True if home page is loaded
        """
        timeout = timeout or 30
        
        self.logger.info("Checking if home page is loaded...")
        
        for indicator in self.HOME_INDICATORS:
            if self.is_displayed(indicator, timeout=5):
                self.logger.info(f"✅ Home page verified via indicator: {indicator}")
                return True
        
        self.logger.warning("⚠️ No home indicators found")
        return False
    
    def wait_for_home_screen(self, timeout=60):
        """
        Wait for the home screen to be fully loaded.
        
        This method handles the initial loading period after login
        where the app may show a loading screen or black screen.
        
        Args:
            timeout: Maximum time to wait in seconds
            
        Returns:
            bool: True if home screen loaded successfully
        """
        self.logger.info(f"Waiting for home screen to load (timeout: {timeout}s)...")
        
        # Force refresh of UI tree
        _ = self.driver.page_source
        
        # Try multiple times with different indicators
        for i in range(1, 13):  # Up to 12 attempts
            self.logger.debug(f"Scan {i}: Checking UI for home indicators...")
            
            # Refresh UI tree
            _ = self.driver.page_source
            
            for indicator in self.HOME_INDICATORS:
                try:
                    elements = self.find_elements(*indicator)
                    if elements and len(elements) > 0:
                        # Verify element is actually displayed (not covered by black screen)
                        if elements[0].is_displayed():
                            self.logger.info(f"✅ Home screen detected and VISIBLE via: {indicator}")
                            return True
                        else:
                            self.logger.debug("Element found but not visible (possibly covered)")
                except Exception as e:
                    self.logger.debug(f"Error checking indicator {indicator}: {e}")
            
            # Wait before next attempt
            self.wait_for_element_gone(
                AppiumBy.XPATH, 
                "//*[contains(@text, 'Loading')] | //*[contains(@text, 'loading')]",
                timeout=5
            )
        
        self.logger.error("❌ Home screen did not load within timeout")
        self.take_screenshot("home_screen_not_loaded")
        return False
    
    def is_home_screen_visible(self):
        """
        Check if the home screen is visible and not covered by overlays.
        
        Returns:
            bool: True if home screen is visible
        """
        try:
            # Check for the primary verification element
            if self.is_displayed(self.HOME_VERIFICATION):
                elements = self.find_elements(*self.HOME_VERIFICATION)
                if elements and len(elements) > 0:
                    return elements[0].is_displayed()
            return False
        except Exception as e:
            self.logger.debug(f"Home screen visibility check failed: {e}")
            return False
    
    # ==================== HOME SCREEN ACTIONS ====================
    
    def get_user_name(self):
        """
        Get the displayed user name on the home screen.
        
        Returns:
            str: User name if found, empty string otherwise
        """
        # Look for user name indicator
        name_locator = (AppiumBy.XPATH, "//android.widget.TextView[contains(@text, 'Trinh')]")
        return self.get_text(name_locator)
    
    def click_profile(self):
        """
        Click on the profile icon.
        
        Returns:
            bool: True if click successful
        """
        self.logger.info("Clicking profile icon")
        return self.click(self.PROFILE_ICON, force=True)
    
    def has_session_indicator(self):
        """
        Check if a session indicator is visible.
        
        Returns:
            bool: True if session indicator is present
        """
        session_locator = (AppiumBy.XPATH, "//*[contains(@text, 'Session 1')]")
        return self.is_displayed(session_locator)
    
    def get_session_count(self):
        """
        Get the number of sessions displayed.
        
        Returns:
            int: Number of sessions found
        """
        session_locator = (AppiumBy.XPATH, "//*[contains(@text, 'Session')]")
        elements = self.find_elements(*session_locator)
        return len(elements)
    
    # ==================== NAVIGATION ====================
    
    def go_to_profile(self):
        """
        Navigate to the profile screen by clicking the profile icon.
        
        Returns:
            bool: True if navigation successful
        """
        self.logger.info("Navigating to profile screen")
        return self.click_profile()
    
    def refresh_home(self):
        """
        Refresh the home screen by pulling down or other means.
        
        Returns:
            bool: True if refresh successful
        """
        self.logger.info("Refreshing home screen")
        return self.swipe_down()