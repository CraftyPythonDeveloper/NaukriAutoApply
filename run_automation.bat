@echo off
setlocal enabledelayedexpansion

:: Check if Python is installed
python --version > nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.9 or higher.
    pause
    exit /b 1
)

:: Check Python version
python -c "import sys; sys.exit(0) if sys.version_info >= (3, 9) else sys.exit(1)" > nul 2>&1
if errorlevel 1 (
    echo Python version 3.9 or higher is required.
    pause
    exit /b 1
)

:: Check if virtual environment exists
if exist .venv (
    echo Virtual environment found, activating...
    call .venv\Scripts\activate.bat
    if errorlevel 1 (
        echo Failed to activate virtual environment.
        pause
        exit /b 1
    )
) else (
    echo Creating new virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo Failed to create virtual environment.
        pause
        exit /b 1
    )
    
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
    if errorlevel 1 (
        echo Failed to activate virtual environment.
        pause
        exit /b 1
    )
    
    echo Installing dependencies...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Failed to install dependencies.
        pause
        exit /b 1
    )
)

:: Check for required files
if not exist .env (
    echo Error: .env file not found. Please create .env file with GEMINI_API_KEY.
    pause
    exit /b 1
)

if not exist resume_data.txt (
    echo Error: resume_data.txt not found. Please add your resume data.
    pause
    exit /b 1
)

:: Set PYTHONPATH to include src directory
set PYTHONPATH=%CD%\src;%PYTHONPATH%

:: Run the automation script
echo Starting Naukri Automation...
python src/main.py
if errorlevel 1 (
    echo An error occurred while running the script.
    pause
    exit /b 1
)

:: Deactivate virtual environment
deactivate

echo Script completed successfully.
pause
exit /b 0
