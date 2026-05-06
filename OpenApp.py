from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
import time

# --- 1. CONFIGURATION ---
options = UiAutomator2Options()
options.platform_name = 'Android'
options.automation_name = 'UiAutomator2'
options.device_name = 'emulator-5554'
options.app = r'C:/app-arm64-v8a-v0.8.1_5-development-release.apk'

# Capability for Webviews
options.set_capability("appium:ensureWebviewsHavePages", True)

# --- 2. INITIALIZE DRIVER ---
print("🚀 Starting Appium Server and launching app...")
driver = webdriver.Remote('http://127.0.0.1:4723', options=options)

try:
    print("⏳ Waiting for app to load...")
    time.sleep(5)


    print("✅ Test script executed successfully!")

except Exception as e:
    print(f"❌ Error occurred: {e}")

finally:
    # --- 4. TERMINATE SESSION ---
    print("🔌 Closing application and session...")
    if 'driver' in locals():
        driver.quit()