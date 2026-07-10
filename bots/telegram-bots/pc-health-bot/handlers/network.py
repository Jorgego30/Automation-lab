import logging
import psutil
import urllib.request
from config import ALLOWED_ID
from telegram import Update
from telegram.ext import ContextTypes 

# Network function creation
async def network(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Security filter
    if not update.effective_chat or update.effective_chat.id != ALLOWED_ID:
        return

    # Send "typing" accion
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    bytes_sent = psutil.net_io_counters().bytes_sent
    bytes_recv = psutil.net_io_counters().bytes_recv

    kb_sent = bytes_sent / (1024)
    kb_recv = bytes_recv / (1024)

    final_bytes_sent = kb_sent/1024
    final_bytes_recv = kb_recv/1024

    try:
        public_IP = urllib.request.urlopen("https://api.ipify.org/", timeout=3).read().decode('utf-8')
    except Exception as e:
        logging.error(f"Error fetching public IP: {e}") 
        public_IP = "Unavailable (Connection Error)"

    data = (
        f"Bytes sent by your computer: {final_bytes_sent:.2f}MB" \
        f"\nBytes received by your computer: {final_bytes_recv:.2f}MB"\
        f"\nYour public IP is: {public_IP}"
    )

    #
    await context.bot.send_message(text=data,chat_id=update.effective_chat.id, parse_mode="Markdown")