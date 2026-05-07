"""
Logout test cases for the MaxmAuto test framework.

Contains test cases for verifying logout functionality including:
- Complete logout flow
- Verification of logged out state
- Re-login after logout
"""

import pytest
import time
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


@pytest.fixture(scope="function")
def logged_in_driver(driver):
    """
    Pytest fixture that ensures user is logged in before test.
    
    Args:
        driver: Appium WebDriver instance (from driver fixture)
        
    Yields:
        tuple: (driver, login_page, home_page)
    """
    logger = get_logger(__name__)
    login_page = LoginPage(driver)
    home_page = HomePage(driver)
    
    # Perform login
    logger.info("Logging in before test...")
    assert login_page.login_with_google(), "Pre-test login failed"
    
    # Wait for home screen
    time.sleep(5)
    assert home_page.wait_for_home_screen(timeout=30), \
        "Home screen did not load after pre-test login"
    
    logger.info("✅ User logged in successfully")
    
    yield driver, login_page, home_page


# ==================== TEST CASES ====================

class TestLogout:
    """
    Test suite for logout functionality.
    
    This class contains test cases that verify the logout flow
    works correctly and the user is properly logged out.
    """
    
    @pytest.mark.logout
    def test_logout_flow(self, logged_in_driver):
        """
        Test Case: TC_LOGOUT_001
        Title: Verify user can logout successfully
        
        Preconditions:
        - User is logged in
        
        Steps:
        1. Click on profile icon
        2. Scroll to find logout option
        3. Click on logout button
        4. Confirm logout on popup
        5. Verify login screen is displayed
        
        Expected Result:
        - User should be logged out
        - Login screen should be displayed
        """
        pytest.currenttest = "TC_LOGOUT_001"
        logger = get_logger(__name__)
        
        driver, login_page, home_page = logged_in_driver
        
        try:
            # Initialize login page for logout (it handles both login and logout)
            login_page = LoginPage(driver)
            
            # Steps 1-4: Perform logout
            logger.info("Performing logout...")
            assert login_page.logout(), "Logout flow failed"
            
            # Step 5: Verify login screen
            logger.info("Verifying login screen is displayed...")
            time.sleep(5)  # Wait for transition
            
            assert login_page.verify_logged_out(), \
                "Login screen not displayed after logout"
            
            logger.info("✅ Test passed: User successfully logged out")
            
        except AssertionError as e:
            logger.error(f"❌ Test failed: {e}")
            driver.save_screenshot(str(Config.SCREENSHOTS_DIR / "test_logout_failure.png"))
            raise
    
    @pytest.mark.logout
    def test_logout_verification(self, logged_in_driver):
        """
        Test Case: TC_LOGOUT_002
        Title: Verify logout state is correct
        
        Preconditions:
        - User is logged in
        
        Steps:
        1. Perform logout
        2. Wait for login screen
        3. Verify Google login button is visible
        4. Verify home screen elements are not accessible
        
        Expected Result:
        - Login screen should show Google login option
        - Home screen elements should not be accessible
        """
        pytest.currenttest = "TC_LOGOUT_002"
        logger = get_logger(__name__)
        
        driver, login_page, home_page = logged_in_driver
        
        try:
            # Perform logout
            logger.info("Performing logout...")
            login_page.logout()
            
            # Wait for transition
            time.sleep(5)
            
            # Verify login screen
            logger.info("Verifying login screen...")
            assert login_page.is_login_page(), \
                "Login page indicators not found after logout"
            
            # Verify home screen is not accessible
            logger.info("Verifying home screen is not accessible...")
            # Home screen should not be visible
            assert not home_page.is_home_screen_visible(), \
                "Home screen should not be visible after logout"
            
            logger.info("✅ Test passed: Logout state verified")
            
        except AssertionError as e:
            logger.error(f"❌ Test failed: {e}")
            driver.save_screenshot(str(Config.SCREENSHOTS_DIR / "test_logout_verification_failure.png"))
            raise
    
    @pytest.mark.logout
    @pytest.mark.relogin
    def test_relogin_after_logout(self, driver):
        """
        Test Case: TC_LOGOUT_003
        Title: Verify user can login again after logout
        
        Steps:
        1. Login with Google
        2. Wait for home screen
        3. Logout
        4. Verify login screen
        5. Login again with Google
        6. Verify home screen is displayed
        
        Expected Result:
        - User should be able to login, logout, and login again successfully
        """
        pytest.currenttest = "TC_LOGOUT_003"
        logger = get_logger(__name__)
        
        try:
            login_page = LoginPage(driver)
            home_page = HomePage(driver)
            
            # Step 1-2: First login
            logger.info("=== First Login ===")
            assert login_page.login_with_google(), "First login failed"
            
            time.sleep(5)
            assert home_page.wait_for_home_screen(timeout=30), \
                "Home screen did not load after first login"
            
            logger.info("✅ First login successful")
            
            # Step 3-4: Logout
            logger.info("\n=== Logout ===")
            assert login_page.logout(), "Logout failed"
            
            time.sleep(5)
            assert login_page.verify_logged_out(), \
                "Login screen not displayed after logout"
            
            logger.info("✅ Logout successful")
            
            # Step 5-6: Second login
            logger.info("\n=== Second Login ===")
            assert login_page.login_with_google(), "Second login failed"
            
            time.sleep(5)
            assert home_page.wait_for_home_screen(timeout=30), \
                "Home screen did not load after second login"
            
            logger.info("✅ Second login successful")
            logger.info("✅ Test passed: Login -> Logout -> Login cycle completed")
            
        except AssertionError as e:
            logger.error(f"❌ Test failed: {e}")
            driver.save_screenshot(str(Config.SCREENSHOTS_DIR / "test_relogin_failure.png"))
            raise
    
    @pytest.mark.logout
    def test_logout_confirmation_dialog(self, logged_in_driver):
        """
        Test Case: TC_LOGOUT_004
        Title: Verify logout confirmation dialog appears
        
        Preconditions:
        - User is logged in
        
        Steps:
        1. Click on profile icon
        2. Click on logout button
        3. Verify confirmation dialog appears
        4. Confirm logout
        5. Verify user is logged out
        
        Expected Result:
        - Confirmation dialog should appear before logout
        - User should be logged out after confirming
        """
        pytest.currenttest = "TC_LOGOUT_004"
        logger = get_logger(__name__)
        
        driver, login_page, home_page = logged_in_driver
        
        try:
            # Steps 1-2: Navigate to logout
            logger.info("Clicking profile icon...")
            login_page.click(login_page.PROFILE_ICON, force=True)
            
            time.sleep(3)
            
            # Swipe to find logout
            logger.info("Swiping to find logout option...")
            login_page.swipe_up()
            
            time.sleep(2)
            
            # Check for logout button
            logger.info("Checking for logout button...")
            assert login_page.is_present(login_page.LOGOUT_BUTTON), \
                "Logout button not found"
            
            # Click logout
            login_page.click(login_page.LOGOUT_BUTTON, force=True)
            
            # Step 3: Verify confirmation dialog
            logger.info("Checking for confirmation dialog...")
            time.sleep(2)
            
            # Check for confirm button (dialog should be visible)
            assert login_page.is_present(login_page.LOGOUT_CONFIRM), \
                "Logout confirmation dialog did not appear"
            
            logger.info("✅ Confirmation dialog appeared")
            
            # Step 4-5: Confirm and verify
            login_page.click(login_page.LOGOUT_CONFIRM, force=True)
            
            time.sleep(5)
            assert login_page.verify_logged_out(), \
                "User not logged out after confirming"
            
            logger.info("✅ Test passed: Logout confirmation dialog verified")
            
        except AssertionError as e:
            logger.error(f"❌ Test failed: {e}")
            driver.save_screenshot(str(Config.SCREENSHOTS_DIR / "test_logout_dialog_failure.png"))
            raise


# ==================== STANDALONE EXECUTION ====================

if __name__ == "__main__":
    # Run tests standalone (without pytest)
    print("Running logout tests standalone...")
    
    driver = DriverFactory.create_driver()
    
    try:
        login_page = LoginPage(driver)
        home_page = HomePage(driver)
        
        # First, login
        print("\n--- Logging In ---")
        if login_page.login_with_google():
            print("✅ Login successful")
            
            time.sleep(5)
            if home_page.wait_for_home_screen():
                print("✅ Home screen loaded")
                
                # Test logout
                print("\n--- Testing Logout ---")
                if login_page.logout():
                    print("✅ Logout completed")
                    
                    time.sleep(3)
                    if login_page.verify_logged_out():
                        print("✅ Verified: User is on login screen")
                    else:
                        print("❌ Verification failed: Not on login screen")
                else:
                    print("❌ Logout failed")
            else:
                print("❌ Home screen did not load")
        else:
            print("❌ Login failed")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        DriverFactory.quit_driver(driver)