import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
from logger_config import setup_logger

logger = setup_logger()

def validate_and_load_resume():
    """Validate resume file exists and load its content"""
    resume_path = Path("../resume_data.txt")
    if not resume_path.exists():
        error_msg = "resume_data.txt not found in root directory. Please add your resume data."
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
        
    try:
        with open(resume_path, 'r', encoding='utf-8') as file:
            resume_content = file.read().strip()
            if not resume_content:
                raise ValueError("resume_data.txt is empty")
            return resume_content
    except Exception as e:
        logger.error(f"Error reading resume data: {str(e)}")
        raise

def setup_gemini():
    """Setup Gemini API with environment variables"""
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        error_msg = "GEMINI_API_KEY not found in .env file"
        logger.error(error_msg)
        raise ValueError(error_msg)
        
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        return model
    except Exception as e:
        logger.error(f"Error setting up Gemini: {str(e)}")
        raise

def create_prompt(question, resume_content, choices=None):
    """Create an effective prompt for Gemini"""
    base_prompt = f"""Based on the following resume content, answer the question EXACTLY and CONCISELY without any explanations.
    if you have choices, then answer must be one of the choices. If asked to upload a resume, the choice must be i'll do it later.
    
Resume Content:
{resume_content}

Question: {question}

Instructions:
1. Provide ONLY the answer, no explanations or additional context
2. For experience, include units (e.g., "5 years")
3. For salary, provide only numbers without currency
4. Answer must be precise and relevant to the question"""

    if choices:
        choices_text = "\n".join([f"- {choice}" for choice in choices])
        base_prompt += f"""

Available Choices:
{choices_text}

Additional Instructions:
1. Select EXACTLY ONE choice from the above options
2. Choice matching is case-insensitive
3. Answer must be one of the provided choices"""

    return base_prompt

def clean_answer(answer):
    """Clean and format the answer"""
    if not answer:
        return ""
    # Remove any explanations or additional context
    answer = answer.split('.')[0].split('\n')[0].strip()
    # Remove common prefixes that Gemini might add
    prefixes_to_remove = ['answer:', 'response:', 'the answer is:', 'based on the resume:']
    for prefix in prefixes_to_remove:
        if answer.lower().startswith(prefix):
            answer = answer[len(prefix):].strip()
    return answer
