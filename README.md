# 🤖 Naukri Auto Apply Bot

Automate your job application process on Naukri.com with this intelligent bot. The bot uses AI to automatically fill out job applications while simulating human-like behavior to avoid detection.

## 👤 Author

**Amit Yadav**
- 📧 Email: amityadav4664@gmail.com
- 💻 GitHub: [CraftyPythonDeveloper](https://github.com/CraftyPythonDeveloper)

## ✨ Features

- 🚀 Automated job application process
- 🧠 AI-powered form filling using Google's Gemini
- 📊 Excel-based job tracking
- 🔄 Resume-based intelligent responses
- 🎯 Smart handling of different application types
- 💾 Chrome profile persistence

## 🛠️ Tech Stack

- **Python 3.9+**: Core programming language
- **Selenium**: Web automation
- **Google Gemini**: AI for answering application questions
- **Pandas**: Excel file handling
- **Chrome WebDriver**: Browser automation
- **python-dotenv**: Environment variable management
- **Logging**: Built-in Python logging with rotation

## 📋 Prerequisites

1. Python 3.9 or higher
2. Google Chrome browser
3. Stable internet connection
4. Google Gemini API key

## � Getting Your Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click on "Get API key" button
3. If you're not signed in, sign in with your Google account
4. Create a new API key or use an existing one
5. Copy the API key - you'll need this for the `.env` file

Note: The API key is free to use with generous quotas. Make sure to keep your API key secure and never share it publicly.

## �📦 Installation

### Windows Users
1. Clone this repository
2. Double-click `run_automation.bat`

### Linux/Mac Users
1. Clone this repository
2. Make the script executable:
   ```bash
   chmod +x run_automation.sh
   ```
3. Run the script:
   ```bash
   ./run_automation.sh
   ```

The installation script will automatically:
- ✅ Check Python version
- ✅ Create virtual environment
- ✅ Install dependencies
- ✅ Validate required files

## 🚀 Setup

1. Create a `.env` file from `.env.example`:
   ```
   GEMINI_API_KEY = "your_api_key_here"
   ```

2. Create `resume_data.txt` with your resume information:
   ```
   Your resume content here...
   ```

3. Create `naukri_jobs.xlsx` with the following columns:
   - url: Job posting URL
   - status: Application status (blank/applied/failed/company site)
   - message: Status message or error details

## 💫 Usage

1. Run the automation script using the provided batch/shell script
2. When prompted, log in to your Naukri.com account
3. Press Enter after logging in
4. The bot will automatically:
   - Process each job from the Excel file
   - Apply to eligible positions
   - Update application status
   - Handle errors gracefully

## 📊 Status Tracking

The bot tracks each job application with the following statuses:

| Status | Description |
|--------|-------------|
| applied | Successfully applied to the job |
| failed | Application failed (with error message) |
| company site | Application requires company website |
| (blank) | Not yet processed |

## 📝 Logging

- Logs are automatically rotated at 3MB
- All actions and errors are logged
- Console output shows important information
- Detailed logs stored in `logs/naukri_automation.log`

## ⚠️ Important Notes

1. **Login Required**: Manual login is required for security
2. **Rate Limiting**: Built-in delays prevent detection
3. **Chrome Profile**: Uses persistent Chrome profile
4. **Error Handling**: Continues despite individual job failures
5. **Data Privacy**: Keep your API key and resume data secure

## 🤝 Contributing

Feel free to:
- 🐛 Report bugs
- 💡 Suggest features
- 🔧 Submit pull requests

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ❓ Troubleshooting

### Common Issues

1. **Chrome Driver Issues**
   ```
   Solution: The script automatically downloads the correct driver
   ```

2. **Virtual Environment Problems**
   ```
   Solution: Delete .venv folder and rerun the script
   ```

3. **API Key Issues**
   ```
   Solution: Ensure GEMINI_API_KEY is correctly set in .env
   ```

4. **Excel File Errors**
   ```
   Solution: Ensure naukri_jobs.xlsx has required columns
   ```

For more issues, check the log file or create an issue on GitHub.


## ⚠️ Disclaimer

This project is for **EDUCATIONAL PURPOSES ONLY**. By using this software you agree that:

1. You will use this tool responsibly and ethically
2. You understand that automated interactions with websites may violate terms of service
3. The creator is NOT LIABLE for any:
   - Account suspensions or bans
   - Misuse of the tool
   - Consequences of automated applications
   - Data loss or other damages
4. You use this software AT YOUR OWN RISK
5. You will comply with all applicable laws and website terms of service