# Add principal libraries 
import logging
import handlers
from config import TOKEN
from telegram import Update
from telegram.ext import ContextTypes 
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

# Create button handler function to display all commands
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    # Debug if not receive a query
    if not query:
        return

    # Sends an alert to telegram about the reception of the click
    await query.answer()
    
    # Redirect each button to their function
    if query.data == '/status':
        await handlers.status(update, context)
    elif query.data == '/uptime':
        await handlers.uptime(update, context)
    elif query.data == '/network':
        await handlers.network(update, context)
    elif query.data == '/top_processes':
        await handlers.top_processes(update, context)
    elif query.data == '/check:thresholds':
        await handlers.check_thresholds(context)

if __name__ == '__main__':
    # Application creation with Bot Token
    application = ApplicationBuilder().token(TOKEN).build()

    if application.job_queue:
        application.job_queue.run_repeating(handlers.check_thresholds, interval=60,first=10)

    # Command creation (Handlers)
    application.add_handler(CommandHandler('start', handlers.start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(CommandHandler('status', handlers.status))
    application.add_handler(CommandHandler('uptime', handlers.uptime))
    application.add_handler(CommandHandler('network', handlers.network))
    application.add_handler(CommandHandler('top_processes', handlers.top_processes))

    # Launch bot in polling mode
    logging.info("Bot iniciado. Presiona Ctrl+C para detenerlo.")
    application.run_polling()