"""
Driver management module for the MaxmAuto test framework.

Provides a factory class for creating and managing Appium WebDriver instances
with proper configuration and cleanup.
"""

from appium import webdriver
from config.config import Config
from utils.logger import get_logger


class DriverFactory:
    """
    Factory class for creating and managing Appium WebDriver instances.
    
    This class handles the initialization of the Appium driver with proper
    configuration, ensuring consistent setup across all tests.
    
    Example:
        >>> driver = DriverFactory.create_driver()
        >>> # use driver
        >>> DriverFactory.quit_driver(driver)
    """
    
    _logger = get_logger(__name__)
    
    @staticmethod
    def create_driver():
        """
        Create and return a new Appium WebDriver instance.
        
        This method initializes the driver with capabilities defined in Config
        and establishes a connection to the Appium server.
        
        Returns:
            webdriver.Remote: Configured Appium WebDriver instance
            
        Raises:
            Exception: If driver creation fails
        """
        try:
            DriverFactory._logger.info("Initializing Appium WebDriver...")
            DriverFactory._logger.info(f"Environment: {Config.ENVIRONMENT}")
            DriverFactory._logger.info(f"Appium URL: {Config.APPIUM_URL}")
            DriverFactory._logger.info(f"Device: {Config.DEVICE_NAME}")
            DriverFactory._logger.info(f"App: {Config.app_path}")
            
            # Get configured capabilities
            options = Config.get_desired_capabilities()
            
            # Create driver instance
            driver = webdriver.Remote(Config.APPIUM_URL, options=options)
            
            # Set implicit wait
            driver.implicitly_wait(Config.IMPLICIT_WAIT)
            
            DriverFactory._logger.info("✅ WebDriver initialized successfully")
            DriverFactory._logger.info(f"Session ID: {driver.session_id}")
            
            return driver
            
        except Exception as e:
            DriverFactory._logger.error(f"❌ Failed to initialize WebDriver: {e}")
            raise
    
    @staticmethod
    def quit_driver(driver):
        """
        Properly quit the WebDriver and end the session.
        
        Args:
            driver: The WebDriver instance to quit
        """
        if driver:
            try:
                DriverFactory._logger.info("Quitting WebDriver...")
                driver.quit()
                DriverFactory._logger.info("✅ WebDriver quit successfully")
            except Exception as e:
                DriverFactory._logger.warning(f"⚠️ Error quitting WebDriver: {e}")
    
    @staticmethod
    def reset_driver(driver):
        """
        Reset the driver to initial state (navigate to app home).
        
        Args:
            driver: The WebDriver instance to reset
        """
        if driver:
            try:
                DriverFactory._logger.info("Resetting driver state...")
                driver.activate_app(Config.package_name)
                DriverFactory._logger.info("✅ Driver reset successfully")
            except Exception as e:
                DriverFactory._logger.warning(f"⚠️ Error resetting driver: {e}")