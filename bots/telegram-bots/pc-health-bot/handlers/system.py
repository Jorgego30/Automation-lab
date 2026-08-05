# Add principal libraries
import psutil
import datetime
import time
import logging
from config import TOKEN, ALLOWED_ID
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes 

# Start function creation
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Security filter
    if not update.effective_chat or update.effective_chat.id != ALLOWED_ID:
        logging.warning(f"Access denied.")
        return
    
    # Second security filter
    if not update.effective_user:
        return

    # Check if the user has his username configurate, if not use his first name in the start message
    if update.effective_user.username == None:
        user_name = update.effective_user.first_name
    else:
        user_name = update.effective_user.username

    # Create the welcome message
    welcome = f"👋 Hello, {user_name}! I'm your System Health bot. Use /status to check server status."

    # Create the display of all buttons with all commands
    keyboard = [
        [
            InlineKeyboardButton("📊 System Status", callback_data='/status'),
            InlineKeyboardButton("⏱️ Uptime", callback_data='/uptime')
        ],
        [
            InlineKeyboardButton("🌐 Network Stats", callback_data='/network'),
            InlineKeyboardButton("⚙️ Top Processes", callback_data='/top_processes')
        ]
    ]

    # Create the reply of the buttons
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Response to autorize user
    await context.bot.send_message(text=welcome, chat_id=update.effective_chat.id, parse_mode="Markdown", reply_markup=reply_markup)

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

    # Conversion of seconds to days
    days_total = int(total_time // 86400)

    # Conversion of seconds to hours
    hours_total = int((total_time % 86400) // 3600)

    # Conversion of seconds to minutes
    minutes_total = int((total_time % 3600) // 60)

    # Create the message with the time
    parse_total_time = f"{days_total}d {hours_total}h {minutes_total}m"

    # Create parse message
    uptime_report = (
        f"📅 *Boot time*: {boot_time}\n"
        f"🕒 *Current time*: {current_time}\n"
        f"⏱️ *Uptime*: {parse_total_time}"
    )

    # Send the message
    await context.bot.send_message(text=uptime_report,chat_id=update.effective_chat.id, parse_mode="Markdown")