# Add principal libraries
import asyncio
from config import ALLOWED_ID
import psutil
from telegram import Update
from telegram.ext import ContextTypes 

# Top process function creation to read the top processes in your cpu
async def top_processes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Security filter
    if not update.effective_chat or update.effective_chat.id != ALLOWED_ID:
        return

    # Send "typing" accion
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")   

    # First read to not receive 0 in the first query
    # Create the list to the first read
    active_procs = [] 

    # Read all processes iterationes of pids and names to catch all processes in your cpu
    for p in psutil.process_iter(['pid', 'name']):
        try:
            p.cpu_percent(interval=None)
            active_procs.append(p)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue            

    # Wait 0.2 seconds
    await asyncio.sleep(0.2)

    # Second read to receive real process reads
    # Create the list to the last read
    procs = []

    # Read all processes iterationes to publish in the message
    for p in active_procs:
        try:
            # Read all cpus
            cpu = p.cpu_percent(interval=None)
            
            # Create the message with pid name and cpu
            procs.append({
                'pid':p.info['pid'],
                'name':p.info['name'],
                'cpu_percent':cpu
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue            

    # Sort all the processes to have the most "expensive" processes first
    sorted_procs = sorted(procs, key=lambda x: x['cpu_percent'], reverse=True)

    # Create the message formated
    report = "Top 5 CPU processes\n"

    # Take only the first 5 processes
    for proc in sorted_procs[:5]:
        cpu = proc['cpu_percent'] if proc['cpu_percent'] is not None else 0.0
        pid = proc['pid']
        name = proc['name']
        
        report += f"`PID: {pid:<6} | CPU: {cpu:>5.1f}% | {name}`\n"

    # Send the message
    await context.bot.send_message(text=report,chat_id=update.effective_chat.id, parse_mode="Markdown")

