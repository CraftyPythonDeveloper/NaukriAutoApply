import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger():
    """Configure logging with rotating file handler"""
    logger = logging.getLogger('naukri_automation')
    logger.setLevel(logging.DEBUG)
    
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Rotating file handler (3MB max size)
    file_handler = RotatingFileHandler(
        'logs/naukri_automation.log',
        maxBytes=3 * 1024 * 1024,  # 3MB
        backupCount=5
    )
    
    # Define log format
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    
    return logger

# Create console handler for immediate feedback
def add_console_handler(logger):
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
