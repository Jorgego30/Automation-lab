import os
import logging
from dotenv import load_dotenv

# Read .env file
load_dotenv()

# Token id
TOKEN = os.getenv("TELEGRAM_TOKEN", "0")

# Chat id
ALLOWED_ID = int(os.getenv("TELEGRAM_CHAT_ID", "0"))

# System logging configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
