"""
Login Page Object for the MaxmAuto test framework.

Represents the login screen of the Maxm app and provides methods
for interacting with login-related UI elements.
"""

from appium.webdriver.common.appiumby import AppiumBy
from config.config import Config
from utils.logger import get_logger
from pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Page Object for the Login screen.
    
    This class represents the login page of the Maxm app and provides
    methods for logging in via Google, entering credentials, and handling
    permission dialogs.
    
    Locators:
        - GOOGLE_BUTTON: Button to initiate Google login
        - EMAIL_INPUT: Input field for email address
        - PASSWORD_INPUT: Input field for password
        - NEXT_BUTTON: Button to proceed to next step
        - AGREE_BUTTON: Button to accept terms/permissions
        - ALLOW_BUTTON: System permission allow button
    """
    
    # ==================== PAGE LOCATORS ====================
    
    # Login options on the app's login screen
    GOOGLE_BUTTON = (AppiumBy.XPATH, "//*[contains(@text, 'Google')]")
    
    # Google sign-in page elements
    EMAIL_INPUT = (AppiumBy.XPATH, "//*[@resource-id='identifierId']")
    PASSWORD_INPUT = (AppiumBy.XPATH, "//android.widget.EditText[@password='true'] | //*[contains(@resource-id, 'password')]")
    NEXT_BUTTON = (AppiumBy.XPATH, "//*[@text='NEXT'] | //*[@text='Tiếp theo']")
    
    # Terms/permissions
    AGREE_BUTTON = (AppiumBy.XPATH, "//*[contains(@text, 'agree')] | //*[contains(@text, 'Agree')] | //*[contains(@text, 'đồng ý')]")
    
    # System permission dialogs
    ALLOW_BUTTON_XPATH = (AppiumBy.XPATH, "//android.widget.Button[@text='Allow']")
    ALLOW_BUTTON_ID = (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_button")
    
    # Profile icon (for logout flow)
    PROFILE_ICON = (AppiumBy.XPATH, "//android.widget.ImageView[@index='4']")
    
    # Logout options
    LOGOUT_BUTTON = (AppiumBy.XPATH, "//*[@text='Log out']")
    LOGOUT_CONFIRM = (AppiumBy.XPATH, "//android.widget.Button[@text='Logout']")
    
    # Login verification
    LOGIN_PAGE_INDICATOR = (AppiumBy.XPATH, "//*[contains(@text, 'Google')]")
    
    def __init__(self, driver):
        """
        Initialize LoginPage with a WebDriver instance.
        
        Args:
            driver: Appium WebDriver instance
        """
        super().__init__(driver)
        self.logger = get_logger(self.__class__.__name__)
    
    # ==================== PAGE VALIDATION ====================
    
    def is_page_loaded(self, timeout=None):
        """
        Check if the login page is loaded.
        
        Args:
            timeout: Maximum time to wait (in seconds)
            
        Returns:
            bool: True if login page is loaded
        """
        return self.is_displayed(self.GOOGLE_BUTTON, timeout)
    
    def is_login_page(self):
        """
        Verify we are on the login page by checking for Google login option.
        
        Returns:
            bool: True if on login page
        """
        return self.is_present(self.GOOGLE_BUTTON)
    
    # ==================== LOGIN ACTIONS ====================
    
    def click_google_button(self):
        """
        Click the Google login button.
        
        Returns:
            bool: True if click successful
        """
        self.logger.info("Clicking Google login button")
        # Try normal click first, fallback to force tap
        if not self.click(self.GOOGLE_BUTTON, force=True):
            self.logger.warning("Google button click failed, using force tap")
            return self.force_tap(0.30, 0.71)
        return True
    
    def enter_email(self, email=None):
        """
        Enter email address in the email field.
        
        Args:
            email: Email address to enter. If None, uses config value.
            
        Returns:
            bool: True if successful
        """
        email = email or Config.EMAIL
        self.logger.info(f"Entering email: {email}")
        return self.send_keys(self.EMAIL_INPUT, email)
    
    def enter_password(self, password=None):
        """
        Enter password in the password field.
        
        Args:
            password: Password to enter. If None, uses config value.
            
        Returns:
            bool: True if successful
        """
        password = password or Config.PASSWORD
        self.logger.info("Entering password")
        return self.send_keys(self.PASSWORD_INPUT, password, clear_first=True)
    
    def click_next(self):
        """
        Click the Next button.
        
        Returns:
            bool: True if click successful
        """
        self.logger.info("Clicking Next button")
        return self.click(self.NEXT_BUTTON, force=True)
    
    def click_agree(self):
        """
        Click the Agree/I Agree button for terms/permissions.
        
        Returns:
            bool: True if click successful
        """
        self.logger.info("Clicking Agree button")
        # Swipe up first to ensure button is visible
        self.swipe_up()
        return self.click(self.AGREE_BUTTON, force=True)
    
    def click_allow_permission(self):
        """
        Click the Allow button on system permission dialogs.
        
        Returns:
            bool: True if permission allowed
        """
        self.logger.info("Clicking Allow on permission dialog")
        
        # Try multiple locators for the Allow button
        locators = [
            self.ALLOW_BUTTON_XPATH,
            self.ALLOW_BUTTON_ID,
        ]
        
        for locator in locators:
            if self.click(locator, timeout=5):
                self.logger.info("✅ Permission allowed")
                return True
        
        self.logger.warning("⚠️ Allow button not found - may not be displayed")
        return False
    
    def check_existing_account(self, email=None):
        """
        Check if there's an existing account saved and select it.
        
        Args:
            email: Email to look for. If None, uses config value.
            
        Returns:
            bool: True if existing account was found and selected
        """
        email = email or Config.EMAIL
        self.logger.info(f"Checking for existing account: {email}")
        
        try:
            account_locator = (AppiumBy.XPATH, f"//*[contains(@text, '{email}')]")
            if self.is_displayed(account_locator, timeout=5):
                self.logger.info(f"Found existing account: {email}")
                return self.click(account_locator)
        except Exception as e:
            self.logger.debug(f"No existing account found: {e}")
        
        return False
    
    # ==================== FULL LOGIN FLOW ====================
    
    def login_with_google(self, email=None, password=None):
        """
        Perform complete Google login flow.
        
        This method handles the entire login process including:
        1. Clicking Google button
        2. Entering email (or selecting existing account)
        3. Entering password
        4. Clicking Agree/Allow on permissions
        
        Args:
            email: Email address. If None, uses config value.
            password: Password. If None, uses config value.
            
        Returns:
            bool: True if login flow completed successfully
        """
        email = email or Config.EMAIL
        password = password or Config.PASSWORD
        
        self.logger.info("Starting Google login flow")
        
        try:
            # Step 1: Click Google button
            self.logger.info("Step 1: Clicking Google button")
            if not self.click_google_button():
                self.logger.error("Failed to click Google button")
                return False
            
            # Wait for Google page to load
            self.wait_for_element(self.EMAIL_INPUT, timeout=30)
            
            # Step 2: Check for existing account or enter email
            self.logger.info("Step 2: Checking for existing account or entering email")
            if not self.check_existing_account(email):
                if not self.enter_email(email):
                    self.logger.error("Failed to enter email")
                    return False
                if not self.click_next():
                    self.logger.error("Failed to click Next after email")
                    return False
            
            # Wait for password field
            self.wait_for_element(self.PASSWORD_INPUT, timeout=20)
            
            # Step 3: Enter password
            self.logger.info("Step 3: Entering password")
            if not self.enter_password(password):
                self.logger.error("Failed to enter password")
                return False
            if not self.click_next():
                self.logger.error("Failed to click Next after password")
                return False
            
            # Step 4: Handle Agree/Allow (may or may not appear)
            self.logger.info("Step 4: Checking for Agree button")
            self.wait_for_element(self.AGREE_BUTTON, timeout=10)
            self.click_agree()
            
            # Step 5: Handle system permissions (may or may not appear)
            self.logger.info("Step 5: Checking for permission dialog")
            self.click_allow_permission()
            
            self.logger.info("✅ Google login flow completed")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Login flow failed: {e}")
            self.take_screenshot("login_failure")
            return False
    
    # ==================== LOGOUT ACTIONS ====================
    
    def logout(self):
        """
        Perform complete logout flow.
        
        This method handles:
        1. Clicking profile icon
        2. Scrolling to and clicking logout
        3. Confirming logout
        
        Returns:
            bool: True if logout successful
        """
        self.logger.info("Starting logout flow")
        
        try:
            # Step 1: Click profile icon
            self.logger.info("Step 1: Clicking profile icon")
            if not self.click(self.PROFILE_ICON, force=True):
                self.logger.warning("Profile icon click failed, using force tap")
                self.force_tap(0.88, 0.10)
            
            # Step 2: Swipe and click logout
            self.logger.info("Step 2: Swiping and clicking logout")
            self.swipe_up()
            if not self.click(self.LOGOUT_BUTTON, force=True):
                self.logger.warning("Logout button click failed, using force tap")
                self.force_tap(0.30, 0.88)
            
            # Step 3: Confirm logout
            self.logger.info("Step 3: Confirming logout")
            if not self.click(self.LOGOUT_CONFIRM, force=True):
                self.logger.warning("Logout confirm click failed, using force tap")
                self.force_tap(0.75, 0.57)
            
            self.logger.info("✅ Logout flow completed")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Logout flow failed: {e}")
            self.take_screenshot("logout_failure")
            return False
    
    def verify_logged_out(self):
        """
        Verify that the user has been logged out by checking for login page.
        
        Returns:
            bool: True if logged out (on login page)
        """
        self.logger.info("Verifying user is logged out")
        return self.is_login_page()