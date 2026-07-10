from config import ALLOWED_ID
import psutil
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes 

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

