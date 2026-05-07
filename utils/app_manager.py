import os
import time
import traceback
from pathlib import Path

from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy

from config.config import Config
from utils.logger import get_logger

logger = get_logger(__name__)


class AppManager:
    """Handle app installation, uninstallation and initial permissions."""

    @staticmethod
    def force_uninstall(package_name: str):
        """Force uninstall with multiple methods"""
        logger.info(f"Force uninstalling: {package_name}")
        
        commands = [
            f"adb uninstall {package_name}",
            f"adb shell pm uninstall -k --user 0 {package_name}",
            f"adb shell pm clear {package_name} 2>nul",
            f"adb shell am force-stop {package_name}"
        ]
        
        for cmd in commands:
            os.system(cmd)
            time.sleep(1)

    @staticmethod
    def clean_reinstall():
        """Uninstall old version and install fresh APK"""
        config = Config()
        logger.info("🔄 Starting clean reinstall...")

        apk_path = config.app_path
        package_name = config.package_name

        if not os.path.exists(apk_path):
            logger.error(f"❌ APK not found: {apk_path}")
            return False

        # Force uninstall
        AppManager.force_uninstall(package_name)

        logger.info(f"Installing APK: {Path(apk_path).name}")
        result = os.system(f'adb install -r "{apk_path}"')

        if result == 0:
            logger.info("✅ App installed successfully!")
            time.sleep(5)
            return True
        else:
            logger.error("❌ Installation failed!")
            return False

    @staticmethod
    def handle_initial_permissions(driver, timeout=60):
        """Super robust permission handler"""
        logger.info("🔎 Handling initial permission dialogs... (timeout 60s)")
        wait = WebDriverWait(driver, timeout)

        # Thêm nhiều locator mạnh hơn + UIAutomator strategy
        locators = [
            (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_button"),
            (AppiumBy.XPATH, "//android.widget.Button[@text='Allow']"),
            (AppiumBy.XPATH, "//android.widget.Button[contains(@text,'Allow')]"),
            (AppiumBy.XPATH, "//android.widget.Button[contains(@text,'CHO PHÉP')]"),
            (AppiumBy.XPATH, "//*[@text='Allow' or contains(@text,'Allow')]"),
            (AppiumBy.XPATH, "//android.widget.Button[@resource-id='android:id/button1']"),
            # UIAutomator strategy (mạnh hơn XPath nhiều trường hợp)
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Allow")'),
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("CHO PHÉP")'),
        ]

        for by, value in locators:
            try:
                logger.info(f"Trying locator: {by} = {value}")
                element = wait.until(EC.element_to_be_clickable((by, value)))
                element.click()
                logger.info(f"✅ SUCCESS Clicked Allow using: {value}")
                time.sleep(3)
                return True
            except Exception as e:
                logger.debug(f"Locator failed: {value} - {str(e)[:100]}")
                continue

        logger.warning("⚠️ Could not find Allow button after all attempts")
        return False

    @classmethod
    def launch_app(cls):
        """Launch giống hệt code cũ của bạn"""
        config = Config()
        logger.info("🚀 Launching app... (matching old script)")

        try:
            options = UiAutomator2Options()
            options.platform_name = 'Android'
            options.automation_name = 'UiAutomator2'
            options.device_name = config.DEVICE_NAME
            options.app = str(config.app_path)

            # === Giữ giống code cũ ===
            options.set_capability("appium:noReset", False)
            options.set_capability("appium:ensureWebviewsHavePages", True)
            options.set_capability("autoGrantPermissions", False)   # Tắt để buộc hiện dialog
            options.set_capability("fullReset", True)
            options.set_capability("newCommandTimeout", 600)

            # Sử dụng trực tiếp string như code cũ
            driver = webdriver.Remote('http://127.0.0.1:4723', options=options)
            
            logger.info("✅ App launched successfully!")
            time.sleep(6)   # Tăng thời gian chờ dialog

            # Debug
            driver.save_screenshot(str(config.SCREENSHOTS_DIR / "after_launch_debug.png"))
            logger.info("📸 Saved debug screenshot")

            cls.handle_initial_permissions(driver, timeout=50)
            return driver

        except Exception as e:
            logger.error(f"❌ Failed to launch app: {e}")
            traceback.print_exc()
            return None