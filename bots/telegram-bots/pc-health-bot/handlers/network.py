# Add principal libraries
import psutil
import urllib.request
from logger import logger
from config import ALLOWED_ID
from telegram import Update
from telegram.ext import ContextTypes 

# Network function creation
async def network(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id if update.effective_user else "Unkown"

    # Security filter
    if not update.effective_chat or update.effective_chat.id != ALLOWED_ID:
        logger.warning(f"Access denied to /network to user: {user_id}")
        return

    logger.info(f"Command /network solicitate by user: {user_id}")

    try:
        # Send "typing" accion
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

        # Take bytes sent by your computer
        bytes_sent = psutil.net_io_counters().bytes_sent
        
        # Take bytes receive by your computer 
        bytes_recv = psutil.net_io_counters().bytes_recv

        # Conversion of bytes sented to kilobytes
        kb_sent = bytes_sent / (1024)

        # Conversion of bytes received to kilobytes
        kb_recv = bytes_recv / (1024)

        # Conversion of kilobytes sented to megabytes
        final_megabytes_sent = kb_sent/1024

        # Conversion of kilobytes received to megabytes
        final_megabytes_recv = kb_recv/1024

        # Obtain your public ip checking if you can connect to the API 
        try:
            public_IP = urllib.request.urlopen("https://api.ipify.org/", timeout=3).read().decode('utf-8')
        # Launch an error if you can't connect to the API
        except Exception as e:
            logger.warning(f"Error fetching public IP: {e}") 
            public_IP = "Unavailable (Connection Error)"

        # Create the parse message to send
        data = (
            f"Bytes sent by your computer: {final_megabytes_sent:.2f}MB" \
            f"\nBytes received by your computer: {final_megabytes_recv:.2f}MB"\
            f"\nYour public IP is: {public_IP}"
        )

        # Send the message
        await context.bot.send_message(text=data,chat_id=update.effective_chat.id, parse_mode="Markdown")
        logger.info(f"Red metrics send to {user_id}")

    except Exception as e:
        logger.error(f"Error executing /network: {e}")