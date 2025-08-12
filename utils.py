import random
import time

def random_delay(min_seconds=1, max_seconds=3):
    """Add a random delay to simulate human behavior"""
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)
    return delay

def wait_for_user_login():
    """Wait for user to login and press Enter"""
    print("\n" + "="*50)
    print("Please login to Naukri.com in the browser")
    print("After logging in, press Enter to continue...")
    print("="*50 + "\n")
    input()  # Wait for user to press Enter

def get_answer(question, choices=None):
    """
    Get answer based on question and choices
    Currently returns 'not available' as per requirements
    To be enhanced with LLM integration in future
    """
    return "not available"
