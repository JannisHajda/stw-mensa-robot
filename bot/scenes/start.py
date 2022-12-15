from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from helper.locales import locales
import db.users as users

keyboard = [
    [
        InlineKeyboardButton("⚙️", callback_data='config'),
        InlineKeyboardButton("🌟", callback_data='favorites'),
        InlineKeyboardButton("🔍", callback_data='search'),
    ]
]


async def scene(update: Update, context: ContextTypes.DEFAULT_TYPE, scene_data):
    query = update.callback_query

    if (query):
        await query.answer()
        await query.edit_message_text(locales['start'], reply_markup=InlineKeyboardMarkup(keyboard))
        return

    await update.message.reply_text(locales['start'], reply_markup=InlineKeyboardMarkup(keyboard))
