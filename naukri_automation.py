import os

from selenium import webdriver
from selenium.common import ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import traceback

import pandas as pd
from logger_config import setup_logger, add_console_handler
from excel_handler import ExcelHandler
from utils import random_delay, wait_for_user_login, get_answer

# Setup logging
logger = setup_logger()
add_console_handler(logger)


class NaukriAutomation:
    def __init__(self):
        self.driver = None
        self.excel_handler = ExcelHandler()
        self.wait_timeout = 10
        
    def setup_driver(self):
        """Initialize and configure Chrome WebDriver"""
        try:
            chrome_options = Options()
            # Add any required Chrome options here
            profile_path = os.path.join(os.getcwd(), "chrome_profile")
            chrome_options.add_argument(f"--user-data-dir={profile_path}")
            chrome_options.add_argument("--profile-directory=Default")

            # Disable password manager popups
            chrome_options.add_experimental_option("prefs", {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "profile.password_manager_leak_detection": False
            })

            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.maximize_window()
            logger.info("WebDriver initialized successfully")
            
        except Exception as e:
            logger.error(f"Error setting up WebDriver: {str(e)}")
            raise
            
    def wait_for_element(self, by, value, timeout=None):
        """Wait for element to be present and visible"""
        timeout = timeout or self.wait_timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            logger.warning(f"Timeout waiting for element: {value}")
            return None
            
    def handle_chat_questions(self):
        """Handle questions in the chat window"""
        try:
            while True:
                # Wait for chat window
                chat_window = self.wait_for_element(By.CLASS_NAME, "chatbot_Drawer.chatbot_right")
                if not chat_window:
                    logger.warning("Chat window is gone")
                    return True

                # Get the latest question
                questions = self.driver.find_elements(By.CLASS_NAME, "botItem.chatbot_ListItem")
                if not questions:
                    logger.info("No more questions to answer")
                    return True
                    
                latest_question = questions[-1].text
                logger.info(f"Processing question: {latest_question}")
                
                # Look for different types of answer inputs
                choices = []
                
                # Check for radio buttons
                radio_container = self.driver.find_elements(By.CLASS_NAME, "ssrc__label")
                if radio_container:
                    choices = [elem.text for elem in radio_container]
                    

                
                # Handle different answer input types
                if radio_container:
                    # Get answer
                    answer = get_answer(latest_question, choices)

                    # Handle radio button selection
                    for radio in radio_container:
                        if radio.text.lower() == answer.lower():
                            radio.click()
                            break
                else:
                    # Check for chips
                    chips = self.driver.find_elements(By.CLASS_NAME, "chatbot_Chip.chipInRow.chipItem")

                    if not chips:
                        chips = self.driver.find_elements(By.XPATH, "//div[@class='multicheckboxes-container']/label")

                    choices = [chip.text for chip in chips]
                    answer = get_answer(latest_question, choices)
                    if chips:
                        for chip in chips:
                            if chip.text.lower() == answer.lower():
                                chip.click()
                                break
                    else:
                        # Try text input
                        text_input = self.driver.find_element(By.CSS_SELECTOR, 'div[data-placeholder="Type message here..."]')
                        if text_input:
                            text_input.send_keys(answer)
                
                # Click save button
                try:
                    save_button = self.wait_for_element(By.CLASS_NAME, "sendMsg")
                    if save_button:
                        save_button.click()
                except ElementClickInterceptedException:
                    logger.warning("Save button click intercepted, retrying...")
                    continue

                random_delay(2, 4)  # Wait between questions
                
        except Exception as e:
            logger.error(f"Error handling chat questions: {str(e)}")
            return False
            
    def process_job(self, url):
        """Process a single job application"""
        try:
            logger.info(f"Processing job URL: {url}")
            self.driver.get(f"https://www.naukri.com{url}")
            random_delay(2, 4)
            
            # Look for apply button
            apply_button = self.wait_for_element(By.ID, "apply-button")
            company_site_button = self.wait_for_element(By.ID, "company-site-button")
            
            if company_site_button and company_site_button.text == "Apply on company site":
                logger.info("Job requires application on company site, skipping...")
                return "company site", "Application needs to be done on company website"
                
            if not apply_button:
                apply_button = self.wait_for_element(By.ID, "already-applied")
                if not apply_button:
                    logger.warning("Apply button not found")
                    return "failed", "Apply button not found on the page"
                
            # Check if job is already applied
            if apply_button.text.strip().lower() == "applied":
                logger.info("Job was already applied previously")
                return "applied", "Already applied to this job"
                
            # Click apply button
            apply_button.click()
            random_delay(1, 2)
            
            # Handle chat questions
            if self.handle_chat_questions():
                logger.info("Successfully completed application")
                return "applied", "Application completed successfully"
            else:
                logger.warning("Failed to complete application process")
                return "failed", "Failed to complete chat questionnaire"
                
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error processing job {url}: {error_msg}")
            return "failed", f"Error: {error_msg}"
            
    def run(self):
        """Main automation loop"""
        try:
            self.setup_driver()
            self.driver.get("https://www.naukri.com")
            
            # Wait for user login
            wait_for_user_login()
            logger.info("User logged in successfully")
            
            # Load jobs from Excel
            jobs_df = self.excel_handler.load_jobs()
            
            # Process each job
            for index, row in jobs_df.iterrows():
                if pd.isna(row['status']) or row['status'] == '':
                    try:
                        status, message = self.process_job(row['url'])
                        self.excel_handler.update_job_status(row['url'], status, message)
                        random_delay(3, 5)  # Wait between jobs
                    except Exception as e:
                        error_msg = str(e)
                        logger.error(f"Error processing job {row['url']}: {error_msg}")
                        traceback.print_exc()
                        self.excel_handler.update_job_status(row['url'], "failed", f"Unexpected error: {error_msg}")
                        continue
                        
        except KeyboardInterrupt:
            logger.info("Script stopped by user")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            traceback.print_exc()
        finally:
            if self.driver:
                self.driver.quit()
                logger.info("Browser closed")

if __name__ == "__main__":
    automation = NaukriAutomation()
    automation.run()
