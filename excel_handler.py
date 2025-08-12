import pandas as pd
import os
from logger_config import setup_logger

logger = setup_logger()

class ExcelHandler:
    def __init__(self, file_path="naukri_jobs.xlsx"):
        self.file_path = file_path
        self.validate_file()
        self.df = None
        
    def validate_file(self):
        """Validate if the Excel file exists and has required columns"""
        if not os.path.exists(self.file_path):
            error_msg = f"Excel file '{self.file_path}' does not exist. Please create the file with 'url' and 'status' columns."
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)
            
        try:
            df = pd.read_excel(self.file_path)
            required_columns = ['url', 'status']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                error_msg = f"Required columns {missing_columns} not found in the Excel file."
                logger.error(error_msg)
                raise ValueError(error_msg)
                
        except Exception as e:
            logger.error(f"Error reading Excel file: {str(e)}")
            raise
            
    def load_jobs(self):
        """Load jobs from Excel file"""
        try:
            self.df = pd.read_excel(self.file_path)
            logger.info(f"Successfully loaded {len(self.df)} jobs from Excel file")
            return self.df
        except Exception as e:
            logger.error(f"Error loading jobs from Excel: {str(e)}")
            raise
            
    def update_job_status(self, url, status):
        """Update job status in Excel file"""
        try:
            if self.df is None:
                self.load_jobs()
                
            # Find the row with matching URL and update status
            self.df.loc[self.df['url'] == url, 'status'] = status
            
            # Save the updated DataFrame to Excel
            self.df.to_excel(self.file_path, index=False)
            logger.info(f"Updated status for job {url} to {status}")
            
        except Exception as e:
            logger.error(f"Error updating job status: {str(e)}")
            raise
