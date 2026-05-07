"""
Central configuration module for the MaxmAuto test framework.

This module contains all configuration settings including:
- Appium server settings
- Device capabilities
- Application paths
- Test credentials
- Timeout settings
- Environment configurations (STG/PROD)
"""

import os
from pathlib import Path


class Config:
    """
    Central configuration class that holds all test settings.
    Supports different environments (STG, PROD) and provides
    configurable options for Appium driver initialization.
    """
    
    # ==================== PROJECT ROOT ====================
    # Get the absolute path to the project root directory
    PROJECT_ROOT = Path(__file__).parent.parent
    
    # ==================== ENVIRONMENT SELECTION ====================
    # Change this to 'PROD' for production environment
    ENVIRONMENT = os.getenv('MAXM_ENV', 'STG')
    
    # ==================== APPIUM SERVER ====================
    APPIUM_HOST = os.getenv('APPIUM_HOST', '127.0.0.1')
    APPIUM_PORT = int(os.getenv('APPIUM_PORT', '4723'))
    APPIUM_URL = f"http://{APPIUM_HOST}:{APPIUM_PORT}"
    
    # ==================== DEVICE CONFIGURATION ====================
    # Lấy từ lệnh: adb devices
    DEVICE_NAME = os.getenv('DEVICE_NAME', 'emulator-5554')
    # Nếu muốn chỉ định rõ AVD name (tùy chọn, hữu ích khi có nhiều emulator)
    AVD_NAME = os.getenv('AVD_NAME', 'pixel_7')
    PLATFORM_NAME = os.getenv('PLATFORM_NAME', 'Android')
    AUTOMATION_NAME = os.getenv('AUTOMATION_NAME', 'UiAutomator2')
    # Platform version của emulator Pixel 7
    PLATFORM_VERSION = os.getenv('PLATFORM_VERSION', '17')
    
    # ==================== APPLICATION PATHS ====================
    # APK file paths for different environments
    APK_PATH_STG = os.getenv(
        'APK_PATH_STG',
        r'C:/app-arm64-v8a-v0.8.1_6-development-release.apk'
    )
    APK_PATH_PROD = os.getenv(
        'APK_PATH_PROD',
        r'C:/app-arm64-v8a-v0.8.1_6-development-release.apk'
    )
    
    # Package names for different environments
    PACKAGE_NAME_STG = "au.com.maxmskate.mobile.stg"
    PACKAGE_NAME_PROD = "au.com.maxmskate.mobile"
    
    @property
    def app_path(self):
        """Get the APK path based on current environment."""
        if self.ENVIRONMENT == 'PROD':
            return self.APK_PATH_PROD
        return self.APK_PATH_STG
    
    @property
    def package_name(self):
        """Get the package name based on current environment."""
        if self.ENVIRONMENT == 'PROD':
            return self.PACKAGE_NAME_PROD
        return self.PACKAGE_NAME_STG
    
    # ==================== APPIUM CAPABILITIES ====================
    # Timeout settings (in milliseconds)
    UIAUTOMATOR2_SERVER_LAUNCH_TIMEOUT = 90000  # 90 seconds
    ANDROID_INSTALL_TIMEOUT = 90000  # 90 seconds
    NEW_COMMAND_TIMEOUT = 900  # 15 minutes
    
    # Capability flags
    AUTO_GRANT_PERMISSIONS = True
    NO_RESET = True  # Don't reset app state between sessions
    FULL_RESET = False  # Set to True for clean install each time
    ENSURE_WEBVIEWS_HAVE_PAGES = True
    
    # UIAutomator2 specific settings
    ENFORCE_XPATH1 = True  # Use XPath 1.0 for better compatibility
    
    # ==================== WAIT TIMEOUTS ====================
    # Explicit wait timeouts (in seconds)
    EXPLICIT_WAIT_SHORT = 10
    EXPLICIT_WAIT_MEDIUM = 25
    EXPLICIT_WAIT_LONG = 35
    
    # Implicit wait (in seconds)
    IMPLICIT_WAIT = 10
    
    # ==================== TEST CREDENTIALS ====================
    # These can be overridden via environment variables for security
    EMAIL = os.getenv('MAXM_EMAIL', 'trinhnguyen210589@gmail.com')
    PASSWORD = os.getenv('MAXM_PASSWORD', 'Tt210589')
    
    # ==================== DIRECTORY PATHS ====================
    # Screenshots directory
    SCREENSHOTS_DIR = PROJECT_ROOT / 'screenshots'
    
    # Logs directory
    LOGS_DIR = PROJECT_ROOT / 'logs'
    
    # Reports directory
    REPORTS_DIR = PROJECT_ROOT / 'reports'
    
    # Data directory
    DATA_DIR = PROJECT_ROOT / 'data'
    
    # ==================== LOGGING CONFIGURATION ====================
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE = LOGS_DIR / f'maxmauto_{ENVIRONMENT.lower()}.log'
    
    # ==================== TEST SETTINGS ====================
    # Delay between actions (in seconds)
    ACTION_DELAY = 1
    SCREENSHOT_ON_FAILURE = True
    
    # Number of retries for flaky operations
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # seconds
    
    # ==================== SWIPE SETTINGS ====================
    # Swipe gesture parameters
    SWIPE_START_Y_PERCENT = 0.8  # Start from 80% of screen height
    SWIPE_END_Y_PERCENT = 0.3    # End at 30% of screen height
    SWIPE_X_PERCENT = 0.5        # Horizontal center (50%)
    SWIPE_DURATION = 100         # Swipe duration in milliseconds
    
    @classmethod
    def create_directories(cls):
        """Create all necessary directories if they don't exist."""
        directories = [
            cls.SCREENSHOTS_DIR,
            cls.LOGS_DIR,
            cls.REPORTS_DIR,
            cls.DATA_DIR
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_desired_capabilities(cls):
        """
        Get Appium desired capabilities as a dictionary.
        
        Returns:
            dict: Capabilities for Appium driver initialization
        """
        from appium.options.android import UiAutomator2Options

        config_instance = cls()
        
        options = UiAutomator2Options()
        options.platform_name = cls.PLATFORM_NAME
        options.automation_name = cls.AUTOMATION_NAME
        options.device_name = cls.DEVICE_NAME
        options.app = str(config_instance.app_path)
        
        options.set_capability("avd", cls.AVD_NAME)                    # Nếu muốn Appium tự start emulator
        options.set_capability("udid", cls.DEVICE_NAME)               # Rất quan trọng cho emulator
        options.set_capability("appium:platformVersion", cls.PLATFORM_VERSION)
        # Set capabilities
        options.set_capability("autoGrantPermissions", cls.AUTO_GRANT_PERMISSIONS)
        options.set_capability("noReset", cls.NO_RESET)
        options.set_capability("fullReset", cls.FULL_RESET)
        options.set_capability("ensureWebviewsHavePages", cls.ENSURE_WEBVIEWS_HAVE_PAGES)
        
        # Timeout settings
        options.set_capability(
            "appium:uiautomator2ServerLaunchTimeout",
            cls.UIAUTOMATOR2_SERVER_LAUNCH_TIMEOUT
        )
        options.set_capability(
            "appium:androidInstallTimeout",
            cls.ANDROID_INSTALL_TIMEOUT
        )
        options.set_capability("appium:newCommandTimeout", cls.NEW_COMMAND_TIMEOUT)
        options.set_capability("appium:settings[enforceXPath1]", cls.ENFORCE_XPATH1)
        
        return options
    
    def __repr__(self):
        return (
            f"<Config environment={self.ENVIRONMENT}, "
            f"app={self.app_path}, "
            f"package={self.package_name}>"
        )