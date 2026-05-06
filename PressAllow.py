from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = UiAutomator2Options()
options.platform_name = 'Android'
options.automation_name = 'UiAutomator2'
options.device_name = 'emulator-5554'
options.app = r'C:/app-arm64-v8a-v0.8.1_5-development-release.apk'


options.set_capability("appium:noReset", True) 

print("🚀 Connecting to Appium Server...")
driver = webdriver.Remote('http://127.0.0.1:4723', options=options)

try:
   
    print("⏳ Searching for 'Allow' button...")
    

    wait = WebDriverWait(driver, 30)
    
    try:
        allow_btn = wait.until(EC.element_to_be_clickable(
            (AppiumBy.XPATH, "//android.widget.button[@text='Allow']")
        ))
        allow_btn.click()
        print("✅ Clicked 'Allow' successfully!")
    except:
        print("⚠️ Could not find 'Allow' button via XPATH. Trying alternative...")
        try:
            allow_id = driver.find_element(by=AppiumBy.ID, value='com.android.permissioncontroller:id/permission_allow_button')
            allow_id.click()
            print("✅ Clicked 'Allow' using Resource ID!")
        except:
            print("❌ 'Allow' button is definitely not there or unreachable.")

    time.sleep(3)
    print("📍 Current screen after clicking Allow.")

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    print("🔌 Finished. Closing in 10s...")
    time.sleep(10)
    driver.quit()