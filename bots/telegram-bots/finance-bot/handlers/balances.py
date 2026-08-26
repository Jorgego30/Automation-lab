from config import ALLOWED_ID
from logger import logger
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes 
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id if update.effective_user else "Unkown"
    # Security filter
    if not update.effective_chat or update.effective_chat.id != ALLOWED_ID:
        logger.warning(f"Denied access to /balances to the ID from user: {user_id}")
        return

    logger.info(f"Command /balances requested by user: {user_id}")

    try:
        # Send "typing" accion
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")   

        message_balances = "Select the action you want to do"
        
        # Create the display of all buttons with all commands
        keyboard = [
            [
                InlineKeyboardButton("Cash Boxes", callback_data='/cash_boxes'),
                InlineKeyboardButton("Profits", callback_data='/profits')
            ],
            [
                InlineKeyboardButton("Deposit", callback_data='/deposit'),
                InlineKeyboardButton("Withdraw", callback_data='/withdraw')
            ],
            [
                InlineKeyboardButton("Return <<", callback_data='/return')
            ]
        ]

        # Create the reply of the buttons
        reply_markup = InlineKeyboardMarkup(keyboard)
    
        # Send the message
        await context.bot.send_message(text=message_balances,chat_id=update.effective_chat.id, parse_mode="Markdown", reply_markup=reply_markup)
        logger.info(f"top_processes sent correctly to {user_id}")

    except Exception as e:
        logger.error(f"Error obtaining or sending top_processes: {e}")

