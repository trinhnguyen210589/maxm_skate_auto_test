"""
Test setup: Clean uninstall + reinstall app
"""
import pytest
import time
from utils.app_manager import AppManager


@pytest.mark.setup
def test_clean_reinstall():
    """Clean install app before running other tests"""
    success = AppManager.clean_reinstall()
    assert success, "❌ Clean reinstall failed!"
    print("✅ Clean reinstall completed successfully")


@pytest.mark.setup
def test_launch_app_with_permissions():
    """Launch app and handle initial permissions - KEEP APP OPEN"""
    driver = AppManager.launch_app()
    assert driver is not None, "❌ Failed to launch app"
    
    print("✅ App launched and permissions handled")
    print("📱 App is now running on emulator...")
    
    # Giữ app mở trong 10 giây để bạn xem
    time.sleep(10)
    
    # KHÔNG quit driver ở đây nếu bạn muốn app vẫn mở
    # driver.quit()   # ← Comment dòng này lại nếu muốn app ở lại