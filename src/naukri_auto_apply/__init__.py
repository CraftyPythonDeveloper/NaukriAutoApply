"""
Naukri Auto Apply - Main package initialization
Author: Amit Yadav
"""

from .automation import NaukriAutomation
from .excel_handler import ExcelHandler
from .utils import random_delay, wait_for_user_login, get_answer
from .gemini_helper import setup_gemini, validate_and_load_resume

__version__ = "0.1.0"
__author__ = "Amit Yadav"
__email__ = "amityadav4664@gmail.com"
