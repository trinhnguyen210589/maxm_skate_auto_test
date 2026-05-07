"""
Screenshot utility module for the MaxmAuto test framework.

Provides functionality to capture, save, and manage screenshots
for test documentation and failure analysis.
"""

import os
from datetime import datetime
from pathlib import Path
from config.config import Config
from utils.logger import get_logger


class ScreenshotHelper:
    """
    Helper class for capturing and managing screenshots during test execution.
    
    This class provides methods to take screenshots and save them to the
    designated screenshots directory with appropriate naming conventions.
    
    Example:
        >>> screenshot = ScreenshotHelper(driver)
        >>> screenshot.capture("login_screen")
    """
    
    _logger = get_logger(__name__)
    
    def __init__(self, driver):
        """
        Initialize ScreenshotHelper with a WebDriver instance.
        
        Args:
            driver: Appium WebDriver instance
        """
        self.driver = driver
        self.screenshot_dir = Config.SCREENSHOTS_DIR
        
        # Ensure screenshot directory exists
        try:
            Config.create_directories()
        except Exception as e:
            self._logger.warning(f"Could not create directories: {e}")
    
    def capture(self, name: str, description: str = "") -> str:
        """
        Capture a screenshot and save it to the screenshots directory.
        
        Args:
            name: Base name for the screenshot file
            description: Optional description to include in filename
            
        Returns:
            str: Path to the saved screenshot, or None if failed
        """
        try:
            # Create filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.png"
            filepath = self.screenshot_dir / filename
            
            # Capture screenshot
            self.driver.save_screenshot(str(filepath))
            
            self._logger.info(f"📸 Screenshot saved: {filepath}")
            
            return str(filepath)
            
        except Exception as e:
            self._logger.error(f"❌ Failed to capture screenshot '{name}': {e}")
            return None
    
    def capture_failure(self, test_name: str) -> str:
        """
        Capture a screenshot specifically for test failure documentation.
        
        Args:
            test_name: Name of the failed test
            
        Returns:
            str: Path to the saved screenshot, or None if failed
        """
        name = f"failure_{test_name}"
        return self.capture(name, "Test failure")
    
    def capture_page(self, page_name: str) -> str:
        """
        Capture a screenshot of a specific page/screen.
        
        Args:
            page_name: Name of the page/screen being captured
            
        Returns:
            str: Path to the saved screenshot, or None if failed
        """
        return self.capture(f"page_{page_name}", f"Page: {page_name}")
    
    def get_recent_screenshot(self, pattern: str = "*.png") -> Path:
        """
        Get the most recent screenshot matching the pattern.
        
        Args:
            pattern: Glob pattern to match files
            
        Returns:
            Path: Path to the most recent screenshot, or None if not found
        """
        try:
            screenshots = list(self.screenshot_dir.glob(pattern))
            if screenshots:
                # Return the most recent file
                return max(screenshots, key=os.path.getctime)
            return None
        except Exception as e:
            self._logger.warning(f"Could not find recent screenshot: {e}")
            return None
    
    def cleanup_old_screenshots(self, days: int = 7) -> int:
        """
        Remove screenshots older than the specified number of days.
        
        Args:
            days: Number of days after which screenshots should be deleted
            
        Returns:
            int: Number of files deleted
        """
        import time
        
        deleted_count = 0
        cutoff_time = time.time() - (days * 86400)  # Convert days to seconds
        
        try:
            for screenshot in self.screenshot_dir.glob("*.png"):
                if screenshot.stat().st_mtime < cutoff_time:
                    screenshot.unlink()
                    deleted_count += 1
                    self._logger.info(f"🗑️ Deleted old screenshot: {screenshot.name}")
        except Exception as e:
            self._logger.warning(f"Error cleaning up old screenshots: {e}")
        
        return deleted_count