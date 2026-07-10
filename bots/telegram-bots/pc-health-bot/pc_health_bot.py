# Libraries imports
import datetime
import os
import logging
import time
import psutil
import urllib.request
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler

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
    
    if not update.effective_user:
        return

    user_name = update.effective_user.username 

    welcome = f"👋 Hello, {user_name}! I'm your System Health bot. Use /status to check server status."

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

    reply_markup = InlineKeyboardMarkup(keyboard)

    # Response to autorize user
    await context.bot.send_message(text=welcome, chat_id=update.effective_chat.id, parse_mode="Markdown", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if not query:
        return

    await query.answer() # Avisa a Telegram que el clic fue recibido
    
    # Redirigimos de forma inteligente según el botón pulsado
    if query.data == '/status':
        await status(update, context)
    elif query.data == '/uptime':
        await uptime(update, context)
    elif query.data == '/network':
        await network(update, context)
    elif query.data == '/top_processes':
        await top_processes(update, context)

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

# Top process function creation
async def top_processes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Security filter
    if not update.effective_chat or update.effective_chat.id != ALLOWED_ID:
        return

    # Send "typing" accion
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")   

    procs = []

    for p in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent']):
        try:
            procs.append(p.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue            

    # Ordenamos de mayor a menor usando la CPU como clave
    procs_ordenados = sorted(procs, key=lambda x: x['cpu_percent'], reverse=True)

    report = "Top 5 CPU processes\n"
    for proc in procs_ordenados[:5]:
        cpu = proc['cpu_percent'] if proc['cpu_percent'] is not None else 0.0
        pid = proc['pid']
        name = proc['name']
        
        report += f"`PID: {pid:<6} | CPU: {cpu:>5.1f}% | {name}`\n"

    await context.bot.send_message(text=report,chat_id=update.effective_chat.id, parse_mode="Markdown")



if __name__ == '__main__':
    # Application creation with Bot Token
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Command creation (Handlers)
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(CommandHandler('status', status))
    application.add_handler(CommandHandler('uptime', uptime))
    application.add_handler(CommandHandler('network', network))
    application.add_handler(CommandHandler('top_processes', top_processes))

    # Launch bot in polling mode
    logging.info("Bot iniciado. Presiona Ctrl+C para detenerlo.")
    application.run_polling()