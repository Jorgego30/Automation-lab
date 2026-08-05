import logging
import psutil
import time
from config import ALLOWED_ID
from telegram.ext import ContextTypes

CPU_THRESHOLD = 90.0
RAM_THRESHOLD = 85.0
DISK_THRESHOLD = 90.0

ALERT_STATE = {
    'cpu' : {'active':False, 'consecutive_hits': 0},
    'ram' : {'active':False},
    'disk' : {'active': False}
}

# Start function creation
async def check_thresholds(context: ContextTypes.DEFAULT_TYPE):
    try:    
        # Psutil variables
        # Cpu use in percentage
        cpu_use = psutil.cpu_percent(interval=None)
        # Ram use in percentage
        ram_use = psutil.virtual_memory().percent
        # Disk use in percentage
        disk_use = psutil.disk_usage('/').percent

        if cpu_use >= CPU_THRESHOLD:
            ALERT_STATE['cpu']['consecutive_hits'] += 1
            if ALERT_STATE['cpu']['consecutive_hits'] >= 3 and not ALERT_STATE['cpu']['active']:
                cpu_alert = f"HIGH CPU USAGE: {cpu_use}%\nCheck your proceses with /top_processes and kill the most expensive"
                await context.bot.send_message(chat_id=ALLOWED_ID, parse_mode="Markdown", text= cpu_alert)
                ALERT_STATE['cpu']['active'] = True
        else:
            ALERT_STATE['cpu']['consecutive_hits'] = 0
            if ALERT_STATE['cpu']['active']:
                msg = f"RESOLVED: CPU usage back to normal {cpu_use}%"
                await context.bot.send_message(chat_id=ALLOWED_ID, text=msg, parse_mode="Markdown")
                ALERT_STATE['cpu']['active'] = False

        if ram_use >= RAM_THRESHOLD:
            if not ALERT_STATE['ram']['active']:
                ram_alert = f"HIGH RAM USAGE: {ram_use}%\nCheck your processes and kill the most expensive"
                await context.bot.send_message(chat_id=ALLOWED_ID, text=msg, parse_mode="Markdown")
                ALERT_STATE['ram']['active'] = True
        elif ALERT_STATE['ram']['active']:
            msg = f"RESOLVED: RAM usage back to normal {ram_use}%"
            await context.bot.send_message(chat_id=ALLOWED_ID, text=msg, parse_mode="Markdown")
            ALERT_STATE['ram']['active'] = False

        if disk_use >= DISK_THRESHOLD:
            if not ALERT_STATE['disk']['active']:
                disk_alert = f"LOW DISK SPACE: {disk_use}%\nCheck your disk usage and try to liberate some space"
                await context.bot.send_message(chat_id=ALLOWED_ID, text=msg, parse_mode="Markdown")
                ALERT_STATE['disk']['active'] = True
        elif ALERT_STATE['disk']['active']:
            msg = f"RESOLVED: Disk usage back to normal {disk_use}%"
            await context.bot.send_message(chat_id=ALLOWED_ID, text=msg, parse_mode="Markdown")
            ALERT_STATE['disk']['active'] = False

    except Exception as e:
        logging.error(f"Error during system threshold check: {e}")
