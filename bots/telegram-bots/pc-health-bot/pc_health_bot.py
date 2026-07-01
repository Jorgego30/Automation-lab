# Libraries imports
import datetime
import os
import logging
import time
import psutil
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler

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

# Start function creation
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Security filter
    if not update.effective_chat or update.effective_chat.id != ALLOWED_ID:
        logging.warning(f"Access denied.")
        return

    # Response to autorize user
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

    # Status report message
    status_report = (
        "Sytem monitor\n" \
        "-------------\n" \
        f"*Cpu use*: {cpu_use}%\n" \
        f"*Ram use*: {ram_use}%\n" \
        f"*Disk use*: {disk_use}%\n"
    )

    # Sending status message
    await context.bot.send_message(text=status_report,  chat_id=update.effective_chat.id, parse_mode="Markdown")

# Uptime function creation
async def uptime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Security filter
    if not update.effective_chat or update.effective_chat.id != ALLOWED_ID:
        return

    # Send "typing" accion
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    # Last time you turn on your computer
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")

    # Current time 
    current_time =  datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")

    # How much time has your computer been turned on
    total_time = time.time()-psutil.boot_time()

    days_total = int(total_time // 86400)
    hours_total = int((total_time % 86400) // 3600)
    minutes_total = int((total_time % 3600) // 60)

    parse_total_time = f"{days_total}d {hours_total}h {minutes_total}m"

    uptime_report = (
        f"📅 *Boot time*: {boot_time}\n"
        f"🕒 *Current time*: {current_time}\n"
        f"⏱️ *Uptime*: {parse_total_time}"
    )

    #
    await context.bot.send_message(text=uptime_report,chat_id=update.effective_chat.id, parse_mode="Markdown")


if __name__ == '__main__':
    # Application creation with Bot Token
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Command creation (Handlers)
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('status', status))
    application.add_handler(CommandHandler('uptime', uptime))
    
    # Launch bot in polling mode
    logging.info("Bot iniciado. Presiona Ctrl+C para detenerlo.")
    application.run_polling()