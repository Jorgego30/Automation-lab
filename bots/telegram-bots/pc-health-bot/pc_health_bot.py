# Libraries imports
import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler

# Read .env file
load_dotenv()

# Token id
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Basic config for the loggin
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
