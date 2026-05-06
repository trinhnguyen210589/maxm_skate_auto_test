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

options.set_capability("appium:uiautomator2ServerLaunchTimeout", 90000)
options.set_capability("appium:androidInstallTimeout", 90000)
options.set_capability("appium:settings[enforceXPath1]", True)
options.set_capability("appium:newCommandTimeout", 900)

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
    time.sleep(20)

    # --- BƯỚC 1: CLICK GOOGLE ---
    print("Step 1: Clicking Google Button")
    try:
        wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//*[contains(@text, 'Google')]"))).click()
    except:
        force_tap(0.30, 0.71)
    
    time.sleep(25) 

    # --- BƯỚC 2: NHẬP EMAIL ---
    print("Step 2: Entering Email")
    try:
        email_el = wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "//*[@resource-id='identifierId']")))
        email_el.send_keys(EMAIL)
        time.sleep(10)
        if driver.is_keyboard_shown(): driver.hide_keyboard()
        driver.find_element(AppiumBy.XPATH, "//*[@text='NEXT'] | //*[@text='Tiếp theo']").click()
        time.sleep(20)
    except:
        force_tap(0.85, 0.91)

    # --- BƯỚC 3: NHẬP PASSWORD ---
    print("Step 3: Entering Password")
    time.sleep(10) 
    try:
        pass_xpath = "//android.widget.EditText[@password='true'] | //*[contains(@resource-id, 'password')]"
        pass_el = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, pass_xpath)))
        pass_el.send_keys(PASSWORD)
        time.sleep(20)
        if driver.is_keyboard_shown(): driver.hide_keyboard()
        driver.find_element(AppiumBy.XPATH, "//*[@text='NEXT'] | //*[@text='Tiếp theo']").click()
        time.sleep(15)
    except:
        force_tap(0.85, 0.91)

    # --- BƯỚC 4: CLICK AGREE ---
    print("Step 4: Clicking I Agree")
    try:
        manual_swipe_up()
        time.sleep(5)
        agree_xpath = "//*[contains(@text, 'agree')] | //*[contains(@text, 'Agree')] | //*[contains(@text, 'đồng ý')]"
        agree_elements = driver.find_elements(AppiumBy.XPATH, agree_xpath)
        if len(agree_elements) > 0:
            agree_elements[-1].click()
            print("✅ Clicked I Agree")
        else:
            force_tap(0.85, 0.91)
    except:
        force_tap(0.85, 0.91)
            
    print("⏳ Waiting for App to load Home data (30s)...")
    time.sleep(30)

    # --- BƯỚC 5: HOME SCREEN (CHIẾN THUẬT MỚI: DÙNG ID) ---
    print("Step 5: Waiting for Home Screen...")
    
    home_found = False
    # Sử dụng kết hợp Text và Class/ID phổ biến của App
    home_indicators = [
        "//android.widget.TextView[contains(@text, 'Trinh')]", # Chỉ tìm chữ Trinh cho ngắn gọn
        "//android.view.View[contains(@content-desc, 'Home')]", # Tìm theo mô tả hình ảnh (nút Home dưới cùng)
        "//*[contains(@text, 'Session 1')]",
        "//android.widget.Button", # Thử tìm bất kỳ button nào (Start Session thường là button)
        "//*[@resource-id='Home']" # Thử tìm theo ID thanh menu
    ]
    
    for i in range(1, 8): # Tăng thêm nhịp quét
        print(f"Line {i}: Scanning UI...")
        # LỆNH QUAN TRỌNG: Buộc Appium cập nhật lại cây thư mục (UI Source)
        _ = driver.page_source 
        
        for xpath in home_indicators:
            if len(driver.find_elements(AppiumBy.XPATH, xpath)) > 0:
                print(f"✅ SUCCESS: Home Screen detected via '{xpath}'!")
                home_found = True
                break
        if home_found: break
        time.sleep(5) 

    if not home_found:
        print("❌ FAILED: Home Screen not detected.")
        driver.save_screenshot("check_ui_again.png")

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    print("\n--- TEST COMPLETE ---")
    input("Nhấn Enter để thoát...")
    driver.quit()