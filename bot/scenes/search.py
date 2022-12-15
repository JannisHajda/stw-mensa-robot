from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import db.canteens as canteens
from helper.locales import locales


def build_keyboard():
    keyboard = []
    temp_keyboard = []

    for canteen in canteens.list():
        canteen_id = canteen[0]
        canteen_name = canteen[2]

        temp_keyboard.append(InlineKeyboardButton(
            canteen_name, callback_data='canteen-' + str(canteen_id)))

        if len(temp_keyboard) > 0 and len(temp_keyboard) % 2 == 0:
            keyboard.append(temp_keyboard)
            temp_keyboard = []

    if len(temp_keyboard) > 0:
        keyboard.append(temp_keyboard)

    keyboard.append([
        InlineKeyboardButton("◀️", callback_data='start'),
    ])

    return keyboard


async def scene(update: Update, context: ContextTypes.DEFAULT_TYPE, scene_data):
    query = update.callback_query
    keyboard = build_keyboard()

    await query.answer()
    await query.edit_message_text(
        locales['search'], reply_markup=InlineKeyboardMarkup(keyboard))
