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

driver = webdriver.Remote('http://127.0.0.1:4723', options=options)
wait = WebDriverWait(driver, 35)

# ===================== CÁC HÀM HỖ TRỢ (PHẢI CÓ) =====================
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

# ===================== QUY TRÌNH LOG OUT =====================
try:
    print("🚀 Bắt đầu quy trình Log out...")
    time.sleep(5)

    # --- BƯỚC 1: CLICK VÀO PROFILE (Hình 1) ---
    print("Step 1: Click Profile icon")
    try:
        # Thử tìm avatar bằng class trước
        profile_el = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//android.widget.ImageView[@index='4']")))
        profile_el.click()
    except:
        # Nếu lỗi thì dùng tọa độ (khung đỏ hình 1)
        force_tap(0.88, 0.10)
    
    time.sleep(5)

    # --- BƯỚC 2: KÉO XUỐNG VÀ CLICK LOG OUT (Hình 2) ---
    print("Step 2: Scroll and Click Log out")
    manual_swipe_up() 
    time.sleep(3)
    
    try:
        # Tìm chữ Log out màu đỏ
        logout_btn = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//*[@text='Log out']")))
        logout_btn.click()
    except:
        # Tọa độ nút Log out hình 2
        force_tap(0.30, 0.88)

    time.sleep(3)

    # --- BƯỚC 3: XÁC NHẬN LOG OUT TRÊN POPUP (Hình 3) ---
    print("Step 3: Confirm Log out on popup")
    try:
        # Click nút Logout màu xanh trên popup
        confirm_btn = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//android.widget.Button[@text='Logout']")))
        confirm_btn.click()
    except:
        # Tọa độ nút Logout màu xanh hình 3
        force_tap(0.75, 0.57)

    # --- BƯỚC 4: KIỂM TRA MÀN HÌNH LOGIN (Hình 4) ---
    print("Step 4: Verifying Login Screen...")
    time.sleep(8)
    
    if "continue with google" in driver.page_source.lower():
        print("✅ SUCCESS: Logged out successfully!")
    else:
        print("⚠️ Warning: Could not verify Login Screen.")

except Exception as e:
    print(f"❌ Error during Log out: {e}")

finally:
    input("\nNhấn Enter để kết thúc...")
    driver.quit()