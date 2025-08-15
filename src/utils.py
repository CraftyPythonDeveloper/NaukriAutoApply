import random
import time
from pathlib import Path

from gemini_helper import setup_gemini, validate_and_load_resume, create_prompt, clean_answer
from logger_config import setup_logger

logger = setup_logger()


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
    Get answer based on question and choices using Gemini AI
    Retries up to 3 times if the answer is not satisfactory
    """

    # Load resume content and setup Gemini (will raise exception if not available)
    resume_content = validate_and_load_resume()
    model = setup_gemini()
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Create prompt and get response from Gemini
            prompt = create_prompt(question, resume_content, choices)
            response = model.generate_content(prompt)
            
            if not response.text:
                logger.warning(f"Empty response from Gemini (attempt {attempt + 1}/{max_retries})")
                continue
                
            answer = clean_answer(response.text)
            
            # Validate answer if choices are provided
            if choices:
                # Case insensitive matching
                choices_lower = [choice.lower() for choice in choices]
                if answer.lower() not in choices_lower:
                    logger.warning(f"Answer '{answer}' not in choices (attempt {attempt + 1}/{max_retries})")
                    continue
                # Return the answer with original case
                answer = choices[choices_lower.index(answer.lower())]
            
            logger.info(f"Got valid answer: {answer}")
            return answer
            
        except Exception as e:
            logger.error(f"Error getting answer (attempt {attempt + 1}/{max_retries}): {str(e)}")
            if attempt == max_retries - 1:
                raise
            
    logger.error("Failed to get valid answer after all retries")
    raise ValueError("Could not get valid answer from Gemini after multiple attempts")
