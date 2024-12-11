"""
Main file to manage scripts
"""

import os
import sys
import arrow
from dotenv import load_dotenv
from sources.utilities import display
from sources.utilities import logs

# Load env variables
try:
    load_dotenv(os.getenv("PROJECT_NAME"))
except FileNotFoundError:
    sys.exit(display.alert(f"Configuration could not be loaded {repr(Exception)}"))

display.clear_screen()

# Initialize logs
logger = logs.init_logger()

# Initialize script info
start_date = arrow.now(os.getenv("TIMEZONE", "Europe/Paris"))
display.start_info(start_date, "Formatting script")

if __name__ == "__main__":
    display.info("Initialized")

    # End script
    display.end_info(start_date)
    sys.exit()
