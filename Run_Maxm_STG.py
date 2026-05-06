import os
import time
import traceback
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy

# ========================== CONFIGURATION ==========================
PACKAGE_NAME = "au.com.maxmskate.mobile.stg"
APK_PATH = r"C:/app-arm64-v8a-v0.8.1_5-development-release.apk"

# ========================== CLEAN REINSTALL ==========================
def clean_reinstall():
    """Uninstall the old app and install a fresh version"""
    print("🔄 Preparing clean environment...")

    if not os.path.exists(APK_PATH):
        print(f"❌ Error: APK file not found at:\n{APK_PATH}")
        return False

    print("1. Uninstalling previous version...")
    os.system(f"adb uninstall {PACKAGE_NAME}")
    os.system(f"adb shell pm clear {PACKAGE_NAME} 2>nul")

    print(f"2. Installing new APK: {os.path.basename(APK_PATH)}")
    result = os.system(f'adb install -r "{APK_PATH}"')

    if result == 0:
        print("✅ App installed successfully!")
        return True
    else:
        print("❌ Installation failed!")
        return False


# ========================== MAIN EXECUTION ==========================
if __name__ == "__main__":
    print("=" * 70)
    print("🚀 Starting Full Process: Uninstall → Install → Launch App → Click Allow")
    print("=" * 70)

    # Step 1: Clean reinstall
    if not clean_reinstall():
        print("⛔ Stopping script due to installation failure.")
        exit(1)

    time.sleep(4)

    # Step 2: Initialize Appium
    print("\n🚀 Initializing Appium session...")

    options = UiAutomator2Options()
    options.platform_name = 'Android'
    options.automation_name = 'UiAutomator2'
    options.device_name = 'emulator-5554'
    options.app = APK_PATH

    # Important capabilities
    options.set_capability("appium:noReset", False)
    options.set_capability("appium:ensureWebviewsHavePages", True)

    try:
        driver = webdriver.Remote('http://127.0.0.1:4723', options=options)
        print("✅ App launched successfully!")

        wait = WebDriverWait(driver, 30)

        print("🔎 Searching for 'Allow' button...")

        clicked = False

        # Multiple reliable locators (best practice)
        locators = [
            # Method 1: XPath by exact text
            (AppiumBy.XPATH, "//android.widget.Button[@text='Allow']"),
            (AppiumBy.XPATH, "//android.widget.Button[contains(@text, 'Allow')]"),

            # Method 2: Support Vietnamese text if needed
            (AppiumBy.XPATH, "//android.widget.Button[contains(@text, 'CHO PHÉP')]"),

            # Method 3: Standard Android permission button
            (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_button"),
            (AppiumBy.ID, "com.android.packageinstaller:id/permission_allow_button"),

            # Method 4: More flexible fallback
            (AppiumBy.XPATH, "//*[@text='Allow' or contains(@text,'Allow') or contains(@text,'CHO PHÉP')]"),
        ]

        for by, value in locators:
            try:
                element = wait.until(EC.element_to_be_clickable((by, value)))
                element.click()
                print(f"✅ Successfully clicked 'Allow' using: {value}")
                clicked = True
                break
            except:
                continue

        if not clicked:
            print("⚠️ Could not find or click the 'Allow' button. It may not appear.")

        time.sleep(5)
        print("📱 App is now running after handling permission.")

    except Exception as e:
        print(f"❌ Error occurred: {e}")
        traceback.print_exc()

    finally:
        print("\n🔌 Closing Appium session...")
        try:
            driver.quit()
        except:
            pass

    print("=" * 70)
    print("🏁 Process completed!")
    print("=" * 70)