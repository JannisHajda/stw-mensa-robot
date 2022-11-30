from helper.config import config
import logging
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, Updater


# commands
from commands.start import cmd as start_cmd

from helper.scene_manager import scene_manager

from helper.updater import update


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = config.env["TELEGRAM_TOKEN"]

if not TOKEN:
    raise ValueError("No token provided")


if __name__ == '__main__':
    bot = ApplicationBuilder().token(TOKEN).build()
    queue = bot.job_queue
    queue.run_once(update, 10)
    queue.run_repeating(update, interval=1800, first=1800)
    bot.add_handler(CommandHandler('start', start_cmd))
    bot.add_handler(CallbackQueryHandler(scene_manager))
    bot.run_polling()
