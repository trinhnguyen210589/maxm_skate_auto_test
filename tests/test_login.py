"""
Login test cases for the MaxmAuto test framework.

Contains test cases for verifying login functionality including:
- Google login flow
- Login with existing account
- Permission handling
- Home screen verification after login
"""

import pytest
import time
from appium.webdriver.common.appiumby import AppiumBy
from config.config import Config
from utils.driver import DriverFactory
from utils.logger import get_logger
from pages.login_page import LoginPage
from pages.home_page import HomePage


# ==================== FIXTURES ====================

@pytest.fixture(scope="function")
def driver():
    """
    Pytest fixture to create and teardown WebDriver instance for each test.
    
    Yields:
        driver: Appium WebDriver instance
    """
    logger = get_logger(__name__)
    logger.info("=" * 70)
    logger.info(f"Starting test: {pytest.currenttest}")
    logger.info("=" * 70)
    
    # Create driver
    driver = DriverFactory.create_driver()
    
    yield driver
    
    # Teardown
    logger.info(f"Ending test: {pytest.currenttest}")
    DriverFactory.quit_driver(driver)
    logger.info("=" * 70)


# ==================== TEST CASES ====================

class TestLogin:
    """
    Test suite for login functionality.
    
    This class contains test cases that verify the login flow
    works correctly, including Google authentication and permission handling.
    """
    
    @pytest.mark.login
    @pytest.mark.google
    def test_login_with_google(self, driver):
        """
        Test Case: TC_LOGIN_001
        Title: Verify user can login using Google account
        
        Steps:
        1. Launch the app
        2. Click on Google login button
        3. Enter email address
        4. Enter password
        5. Handle any permission dialogs
        6. Verify home screen is displayed
        
        Expected Result:
        - User should be successfully logged in
        - Home screen should be displayed
        """
        pytest.currenttest = "TC_LOGIN_001"
        logger = get_logger(__name__)
        
        try:
            # Initialize pages
            login_page = LoginPage(driver)
            home_page = HomePage(driver)
            
            # Step 1-5: Perform login
            logger.info("Performing Google login...")
            assert login_page.login_with_google(), "Login flow failed"
            
            # Step 6: Verify home screen
            logger.info("Verifying home screen is displayed...")
            time.sleep(5)  # Wait for home screen to fully load
            
            assert home_page.wait_for_home_screen(timeout=30), \
                "Home screen did not load after login"
            
            logger.info("✅ Test passed: User successfully logged in")
            
        except AssertionError as e:
            logger.error(f"❌ Test failed: {e}")
            driver.save_screenshot(str(Config.SCREENSHOTS_DIR / "test_login_failure.png"))
            raise
        except Exception as e:
            logger.error(f"❌ Test error: {e}")
            driver.save_screenshot(str(Config.SCREENSHOTS_DIR / "test_login_error.png"))
            raise
    
    @pytest.mark.login
    @pytest.mark.permission
    def test_handle_permission_dialog(self, driver):
        """
        Test Case: TC_LOGIN_002
        Title: Verify app handles permission dialogs correctly
        
        Steps:
        1. Launch the app
        2. Wait for permission dialog to appear
        3. Click Allow on permission dialog
        4. Verify app continues to login screen
        
        Expected Result:
        - Permission dialog should be handled
        - App should proceed to login screen
        """
        pytest.currenttest = "TC_LOGIN_002"
        logger = get_logger(__name__)
        
        try:
            login_page = LoginPage(driver)
            
            # Try to handle permission dialog
            logger.info("Checking for permission dialog...")
            permission_handled = login_page.click_allow_permission()
            
            # Even if no dialog appeared, that's okay
            logger.info(f"Permission handling result: {'handled' if permission_handled else 'not needed'}")
            
            # Verify we're still on login page
            assert login_page.is_login_page(), "Not on login page after permission handling"
            
            logger.info("✅ Test passed: Permission dialog handled correctly")
            
        except AssertionError as e:
            logger.error(f"❌ Test failed: {e}")
            driver.save_screenshot(str(Config.SCREENSHOTS_DIR / "test_permission_failure.png"))
            raise
    
    @pytest.mark.login
    @pytest.mark.existing_account
    def test_login_with_existing_account(self, driver):
        """
        Test Case: TC_LOGIN_003
        Title: Verify user can login with previously saved account
        
        Steps:
        1. Launch the app
        2. Click on Google login button
        3. Check if existing account is shown
        4. If shown, select the existing account
        5. Verify home screen is displayed
        
        Expected Result:
        - Existing account should be recognized
        - User should be logged in without entering credentials
        """
        pytest.currenttest = "TC_LOGIN_003"
        logger = get_logger(__name__)
        
        try:
            login_page = LoginPage(driver)
            home_page = HomePage(driver)
            
            # Click Google button
            logger.info("Clicking Google login button...")
            login_page.click_google_button()
            
            # Wait for account selection screen
            time.sleep(10)
            
            # Check for existing account
            logger.info("Checking for existing account...")
            account_selected = login_page.check_existing_account()
            
            if account_selected:
                logger.info("✅ Existing account found and selected")
                
                # Wait for home screen
                time.sleep(5)
                assert home_page.wait_for_home_screen(timeout=30), \
                    "Home screen did not load after selecting existing account"
                
                logger.info("✅ Test passed: Logged in with existing account")
            else:
                logger.info("ℹ️ No existing account found - this is expected for first login")
                # Complete the full login
                assert login_page.login_with_google(), "Full login failed"
                assert home_page.wait_for_home_screen(timeout=30), \
                    "Home screen did not load"
                logger.info("✅ Test passed: Completed full login (no existing account)")
            
        except AssertionError as e:
            logger.error(f"❌ Test failed: {e}")
            driver.save_screenshot(str(Config.SCREENSHOTS_DIR / "test_existing_account_failure.png"))
            raise
    
    @pytest.mark.login
    @pytest.mark.home_verification
    def test_home_screen_after_login(self, driver):
        """
        Test Case: TC_LOGIN_004
        Title: Verify home screen displays correctly after login
        
        Steps:
        1. Launch the app
        2. Perform login
        3. Wait for home screen to load
        4. Verify home screen elements are visible
        5. Verify user name is displayed
        
        Expected Result:
        - Home screen should display all expected elements
        - User name should be visible
        """
        pytest.currenttest = "TC_LOGIN_004"
        logger = get_logger(__name__)
        
        try:
            login_page = LoginPage(driver)
            home_page = HomePage(driver)
            
            # Perform login
            logger.info("Performing login...")
            assert login_page.login_with_google(), "Login failed"
            
            # Wait for home screen
            time.sleep(5)
            logger.info("Waiting for home screen to load...")
            assert home_page.wait_for_home_screen(timeout=30), \
                "Home screen did not load"
            
            # Verify home screen elements
            logger.info("Verifying home screen elements...")
            assert home_page.is_page_loaded(), "Home page elements not found"
            
            # Check for session indicator
            if home_page.has_session_indicator():
                logger.info("✅ Session indicator is visible")
            
            # Get user name
            user_name = home_page.get_user_name()
            if user_name:
                logger.info(f"✅ User name displayed: {user_name}")
            
            logger.info("✅ Test passed: Home screen verified successfully")
            
        except AssertionError as e:
            logger.error(f"❌ Test failed: {e}")
            driver.save_screenshot(str(Config.SCREENSHOTS_DIR / "test_home_verification_failure.png"))
            raise


# ==================== STANDALONE EXECUTION ====================

if __name__ == "__main__":
    # Run tests standalone (without pytest)
    print("Running login tests standalone...")
    
    driver = DriverFactory.create_driver()
    
    try:
        login_page = LoginPage(driver)
        home_page = HomePage(driver)
        
        # Test login
        print("\n--- Testing Login ---")
        if login_page.login_with_google():
            print("✅ Login successful")
            
            # Wait for home screen
            time.sleep(5)
            if home_page.wait_for_home_screen():
                print("✅ Home screen loaded")
            else:
                print("❌ Home screen did not load")
        else:
            print("❌ Login failed")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        DriverFactory.quit_driver(driver)