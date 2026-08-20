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
    welcome = f"👋 Hello, {user_name}! I'm your Finance Tracker Health bot. Use /balance to check your account balance."

    # # Create the display of all buttons with all commands
    # keyboard = [
    #     [
    #         InlineKeyboardButton("📊 System Status", callback_data='/status'),
    #         InlineKeyboardButton("⏱️ Uptime", callback_data='/uptime')
    #     ],
    #     [
    #         InlineKeyboardButton("🌐 Network Stats", callback_data='/network'),
    #         InlineKeyboardButton("⚙️ Top Processes", callback_data='/top_processes')
    #     ]
    # ]

    # # Create the reply of the buttons
    # reply_markup = InlineKeyboardMarkup(keyboard)

    # Response to autorize user
    await context.bot.send_message(text=welcome, chat_id=update.effective_chat.id, parse_mode="Markdown")

