# Libraries imports
import os
import logging
import psutil
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

# Start function creation
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Security filter
    if not update.effective_chat or update.effective_chat.id != ALLOWED_ID:
        return
    
    # Send "typing" accion
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    # Psutil variables
    # Cpu use in percentage
    cpu_use = psutil.cpu_percent(interval=1)
    # Ram use in percentage
    ram_use = psutil.virtual_memory().percent
    # Disk use in percentage
    disk_use = psutil.disk_usage('/').percent

    report = (
        "Sytem monitor\n" \
        "-------------\n" \
        f"*Cpu use*: {cpu_use}%\n" \
        f"*Ram use*: {ram_use}%\n" \
        f"*Disk use*: {disk_use}%\n"
    )

    await context.bot.send_message(text=report,  chat_id=update.effective_chat.id, parse_mode="Markdown")

    