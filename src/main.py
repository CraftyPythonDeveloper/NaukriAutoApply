"""
Main entry point for the Naukri Auto Apply bot
"""

from naukri_auto_apply.automation import NaukriAutomation

def main():
    automation = NaukriAutomation()
    automation.run()

if __name__ == "__main__":
    main()
