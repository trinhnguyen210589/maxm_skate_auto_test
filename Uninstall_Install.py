import os

# Configuration for MAxm STG app
PACKAGE_NAME = "au.com.maxmskate.mobile.stg"
# Specific path to your staging build
APK_FILE_PATH = "C:/app-arm64-v8a-v0.8.1_5-development-release.apk"

def clean_reinstall():
    """
    Uninstalls the existing app and performs a fresh installation.
    This ensures no residual data affects the next test run.
    """
    print(f"--- Preparing clean environment for: {PACKAGE_NAME} ---")
    
    # Check if the APK file exists before proceeding
    if not os.path.exists(APK_FILE_PATH):
        print(f"!!! Error: APK file missing at {APK_FILE_PATH}")
        return

    # Step 1: Remove the old version and clear all user data
    print("1. Uninstalling current application...")
    os.system(f"adb uninstall {PACKAGE_NAME}")
    
    # Step 2: Install the new build
    print(f"2. Installing build: {os.path.basename(APK_FILE_PATH)}")
    # Using quotes to handle any potential spaces in the file path
    result = os.system(f"adb install \"{APK_FILE_PATH}\"")
    
    if result == 0:
        print("--- Success: App re-installed. Ready for Driver initialization. ---")
    else:
        print("!!! Failure: Installation failed. Check device connection.")

if __name__ == "__main__":
    clean_reinstall()