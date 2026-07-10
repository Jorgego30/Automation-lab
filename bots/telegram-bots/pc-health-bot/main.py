import logging
import handlers
from config import TOKEN
from telegram import Update
from telegram.ext import ContextTypes 


from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if not query:
        return

    await query.answer() # Avisa a Telegram que el clic fue recibido
    
    # Redirigimos de forma inteligente según el botón pulsado
    if query.data == '/status':
        await handlers.status(update, context)
    elif query.data == '/uptime':
        await handlers.uptime(update, context)
    elif query.data == '/network':
        await handlers.network(update, context)
    elif query.data == '/top_processes':
        await handlers.top_processes(update, context)

if __name__ == '__main__':
    # Application creation with Bot Token
    application = ApplicationBuilder().token(TOKEN).build()
    
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