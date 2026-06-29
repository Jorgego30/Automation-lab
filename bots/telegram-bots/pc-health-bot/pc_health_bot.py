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

# Chat id
ALLOWED_ID = int(os.getenv("TELEGRAM_CHAT_ID", "0"))

# System logging configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Start function creation
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Security filter
    if not update.effective_chat or update.effective_chat.id != ALLOWED_ID:
        logging.warning(f"Access denied.")
        return

    # 2. Responder al usuario autorizado
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="👋 Hello, Jorge! I'm your System Health bot. Use /status to check server status."
    )