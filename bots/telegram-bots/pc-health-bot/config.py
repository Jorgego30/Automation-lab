# Add princpial libraries
import os
from logger import logger
from dotenv import load_dotenv

# Read .env file
load_dotenv()

# Token id
TOKEN = os.getenv("TELEGRAM_TOKEN", "0")

# Chat id
ALLOWED_ID_STR = os.getenv("TELEGRAM_CHAT_ID", "0")

try:
    # Convert ID to an int
    ALLOWED_ID = int(ALLOWED_ID_STR)
except ValueError:
    # Logs for an exception reading the ID
    logger.error("TELEGRAM_CHAT_ID valor in .env isn't a correct int")
    ALLOWED_ID = 0

# Check if the TOKEN in the config file is valid
if TOKEN == "0" or not TOKEN:
    logger.error("TELEGRAM_TOKEN isn't defined or is invalid in .env file")
elif ALLOWED_ID == 0:
    logger.warning("TELEGRAM_CHAT_ID isn't defined or is invalid in .env file")
else:
    # Log to register a correct TOKEN in .env
    logger.info("Configuration correctly from .env")