"""
Logging utility for MaxmAuto framework - FIXED & IMPROVED
"""

import logging
import sys
from config.config import Config


def get_logger(name: str):
    """Get configured logger with console + file output."""
    logger = logging.getLogger(name)
    
    # Tránh duplicate handlers
    if logger.handlers:
        return logger
    
    # Set level từ config
    log_level = getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # Formatter
    formatter = logging.Formatter(Config.LOG_FORMAT)
    
    # === CONSOLE HANDLER (rất quan trọng) ===
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)        # Luôn show DEBUG ra console khi dev
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # === FILE HANDLER ===
    try:
        Config.create_directories()
        file_handler = logging.FileHandler(Config.LOG_FILE, encoding='utf-8', mode='a')
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"⚠️ Warning: Cannot create log file: {e}")
    
    return logger