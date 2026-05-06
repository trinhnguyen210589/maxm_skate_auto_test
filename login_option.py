from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
import time

# ===================== CẤU HÌNH (CONFIGURATION) =====================
options = UiAutomator2Options()
options.platform_name = 'Android'
options.automation_name = 'UiAutomator2'
options.device_name = 'emulator-5554'
options.app = r'C:/app-arm64-v8a-v0.8.1_6-development-release.apk'
options.set_capability("autoGrantPermissions", True)
options.set_capability("noReset", True) 

# Tăng các tham số chờ để tránh treo khi khởi tạo session
options.set_capability("appium:uiautomator2ServerLaunchTimeout", 90000)
options.set_capability("appium:androidInstallTimeout", 90000)
options.set_capability("appium:newCommandTimeout", 900)

# Khởi tạo driver - Hãy để code chạy, đừng nhấn Ctrl+C quá sớm
driver = webdriver.Remote('http://127.0.0.1:4723', options=options)
wait = WebDriverWait(driver, 35)

EMAIL = "trinhnguyen210589@gmail.com"
PASSWORD = "Tt210589"

def force_tap(x_pct, y_pct):
    size = driver.get_window_size()
    x = int(size['width'] * x_pct)
    y = int(size['height'] * y_pct)
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(x, y)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.pause(0.1)
    actions.w3c_actions.pointer_action.release()
    actions.perform()

def manual_swipe_up():
    size = driver.get_window_size()
    start_x = size['width'] / 2
    start_y = size['height'] * 0.8
    end_y = size['height'] * 0.3
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.move_to_location(start_x, end_y)
    actions.w3c_actions.pointer_action.release()
    actions.perform()

try:
    print("🚀 Starting Full Login Sequence...")
    time.sleep(10)

    # --- BƯỚC 1: CLICK GOOGLE ---
    print("Step 1: Clicking Google Button")
    try:
        wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//*[contains(@text, 'Google')]"))).click()
    except:
        force_tap(0.30, 0.71)
    
    time.sleep(15) 

    # --- BƯỚC 1.5: KIỂM TRA TÀI KHOẢN CÓ SẴN ---
    print("Step 1.5: Checking for existing accounts")
    account_selected = False
    try:
        account_xpath = f"//*[contains(@text, '{EMAIL}')]"
        existing_accounts = driver.find_elements(AppiumBy.XPATH, account_xpath)
        if len(existing_accounts) > 0:
            print(f"✅ Found existing account: {EMAIL}. Selecting it...")
            existing_accounts[0].click()
            account_selected = True
            time.sleep(15)
        else:
            print("🔍 No existing account found. Proceeding to manual login.")
    except:
        pass

    # --- BƯỚC 2: NHẬP EMAIL ---
    if not account_selected:
        print("Step 2: Entering Email")
        try:
            email_el = wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//*[@resource-id='identifierId']")))
            email_el.send_keys(EMAIL)
            time.sleep(5)
            driver.find_element(AppiumBy.XPATH, "//*[@text='NEXT'] | //*[@text='Tiếp theo']").click()
            time.sleep(10)
        except:
            force_tap(0.85, 0.91)

    # --- BƯỚC 3: NHẬP PASSWORD ---
    if not account_selected:
        print("Step 3: Entering Password")
        try:
            pass_xpath = "//android.widget.EditText[@password='true'] | //*[contains(@resource-id, 'password')]"
            pass_el = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, pass_xpath)))
            pass_el.send_keys(PASSWORD)
            time.sleep(5)
            driver.find_element(AppiumBy.XPATH, "//*[@text='NEXT'] | //*[@text='Tiếp theo']").click()
            time.sleep(10)
        except:
            force_tap(0.85, 0.91)

    # --- BƯỚC 4: CLICK AGREE ---
    print("Step 4: Checking for I Agree")
    try:
        driver.update_settings({"waitForIdleTimeout": 500}) 
        agree_xpath = "//*[contains(@text, 'agree')] | //*[contains(@text, 'Agree')] | //*[contains(@text, 'đồng ý')]"
        agree_elements = driver.find_elements(AppiumBy.XPATH, agree_xpath)
        if len(agree_elements) > 0:
            manual_swipe_up()
            time.sleep(2)
            agree_elements[-1].click()
            print("✅ Clicked I Agree")
    except:
        force_tap(0.85, 0.91)
            
    print("⏳ Waiting for App to load Home data...")

    # --- BƯỚC 5: HOME SCREEN (CHỈ SỬA Ở ĐÂY ĐỂ TRÁNH NHẬN NHẦM) ---
    print("Step 5: Waiting for Home Screen...")
    home_found = False
    # Dùng text đặc thù chỉ có ở Home, ví dụ: 'Start Session 1'
    home_xpath = "//*[contains(@text, 'Start Session 1')]"
    
    for i in range(1, 21):
        print(f"Nhịp quét {i}: Đang kiểm tra giao diện Home thực sự...")
        try:
            elements = driver.find_elements(AppiumBy.XPATH, home_xpath)
            if len(elements) > 0:
                # KIỂM TRA QUAN TRỌNG: Phần tử phải thực sự hiển thị (không bị màn đen che)
                if elements[0].is_displayed():
                    print(f"✅ SUCCESS: Home Screen detected and VISIBLE!")
                    home_found = True
                    break
                else:
                    print("⏳ Đã thấy phần tử Home nhưng nó đang bị màn hình đen che khuất...")
            else:
                print("⏳ Vẫn đang màn hình load/đen...")
        except:
            print("⚠️ Hệ thống đang bận load dữ liệu, thử lại sau 5s...")
            
        time.sleep(5) 

    if not home_found:
        print("❌ FAILED: Home Screen not detected.")

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    print("\n--- TEST COMPLETE ---")
    input("Nhấn Enter để thoát...")
    driver.quit()