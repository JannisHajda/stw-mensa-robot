from telegram import Update
from telegram.ext import ContextTypes
import db.canteens as canteens
import db.users as users
import db.db as db

from scenes.start import scene as start_scene


async def cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    scene_data = update.message.text.split(' ')[1:]

    await start_scene(update, context, scene_data)
