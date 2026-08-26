from config import ALLOWED_ID
from logger import logger
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes 
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id if update.effective_user else "Unkown"
    # Security filter
    if not update.effective_chat or update.effective_chat.id != ALLOWED_ID:
        logger.warning(f"Denied access to /cash_boxes to the ID from user: {user_id}")
        return

    logger.info(f"Command /cash_boxes requested by user: {user_id}")

    try:
        # Send "typing" accion
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")   

        # Mostrar las huchas creadas con el dinero que hay en cada una, agregar boton de volver
             
        # Send the message
        # await context.bot.send_message(text=report,chat_id=update.effective_chat.id, parse_mode="Markdown")
        logger.info(f"Cash boxes sent correctly to {user_id}")

    except Exception as e:
        logger.error(f"Error obtaining or sending cash boxes: {e}")

async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id if update.effective_user else "Unkown"
    # Security filter
    if not update.effective_chat or update.effective_chat.id != ALLOWED_ID:
        logger.warning(f"Denied access to /cash_boxes to the ID from user: {user_id}")
        return

    logger.info(f"Command /cash_boxes requested by user: {user_id}")

    try:
        # Send "typing" accion
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")   

        # Mostrar las huchas creadas con el dinero que hay en cada una, agregar boton de volver
             
        # Send the message
        # await context.bot.send_message(text=report,chat_id=update.effective_chat.id, parse_mode="Markdown")
        logger.info(f"Cash boxes sent correctly to {user_id}")

    except Exception as e:
        logger.error(f"Error obtaining or sending cash boxes: {e}")