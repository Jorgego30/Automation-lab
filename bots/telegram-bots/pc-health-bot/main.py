# Add principal libraries 
import handlers
from logger import logger
from config import TOKEN
from telegram import Update
from telegram.ext import ContextTypes 
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from telegram.request import HTTPXRequest
import socket

# Forzar resolución IPv4 a nivel global de Python
_old_getaddrinfo = socket.getaddrinfo
def _only_ipv4_getaddrinfo(*args, **kwargs):
    kwargs['family'] = socket.AF_INET
    return _old_getaddrinfo(*args, **kwargs)

socket.getaddrinfo = _only_ipv4_getaddrinfo

# Create button handler function to display all commands
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    # Debug if not receive a query
    if not query:
        logger.warning("CallbackQueryHandler received but query is None")
        return

    # Sends an alert to telegram about the reception of the click
    await query.answer()

    user_id = update.effective_user.id if update.effective_user else "Unkown"
    logger.info(f"Button press: '{query.data}' by user {user_id}")

    try:
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
        else:
            logger.warning(f"Callback data no recognized: {query.data}")
    except Exception as e:
            logger.error(f"Error touching button {query.data}: {e}", exc_info=True)

if __name__ == '__main__':
    # Configuración de red para el cliente HTTPX de Telegram
    request_config = HTTPXRequest(
        connect_timeout=20.0,
        read_timeout=20.0
    )

    # Application creation with Bot Token and HTTPX configuration
    application = (
        ApplicationBuilder()
        .token(TOKEN)
        .request(request_config)
        .build()
    )

    if application.job_queue:
        logger.info("Configurating JobQueue to check alerts")
        application.job_queue.run_repeating(handlers.check_thresholds, interval=10,first=3)
    else:
        logger.warning("JobQueue not available")
        
    # Command creation (Handlers)
    application.add_handler(CommandHandler('start', handlers.start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(CommandHandler('status', handlers.status))
    application.add_handler(CommandHandler('uptime', handlers.uptime))
    application.add_handler(CommandHandler('network', handlers.network))
    application.add_handler(CommandHandler('top_processes', handlers.top_processes))

    # Launch bot in polling mode
    logger.info("Bot running. Kill it with Ctrl+C")
    application.run_polling()