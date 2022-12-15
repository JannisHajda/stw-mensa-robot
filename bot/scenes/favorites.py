from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import db.users as users
import db.canteens as canteens
import json
from helper.build_menu_message import build_message
from helper.locales import locales


def build_keyboard(canteens_available):
    if canteens_available:
        keyboard = [
            [
                InlineKeyboardButton(
                    "🔄", callback_data='favorites-refresh'),
                InlineKeyboardButton("◀️", callback_data='start'),
            ]
        ]
    else:
        keyboard = [
            [
                InlineKeyboardButton("◀️", callback_data='start'),
            ]
        ]

    return keyboard


def build_combined_message(followed_canteens, detailed=False):
    message = ""

    for canteen in followed_canteens:
        canteen_id = canteen[0]
        canteen = canteens.get(canteen_id)
        canteen_name = canteen[2]
        canteen_menu = canteen[4]

        if canteen_menu:
            menu_message = build_message(canteen_name, canteen_menu, detailed)
            message += menu_message

    return message


async def scene(update: Update, context: ContextTypes.DEFAULT_TYPE, scene_data):
    query = update.callback_query

    if (query):
        user_id = query.from_user.id
        user = users.get(user_id)
        detailed = user[2]
        followed_canteens = users.following(user_id)
        keyboard = build_keyboard(len(followed_canteens) > 0)

        if (len(scene_data) > 0):
            command = scene_data[0]

            if command == 'refresh':
                if len(followed_canteens) > 0:
                    message = build_combined_message(
                        followed_canteens, detailed)

                    if query.message.text.split() != message.split():
                        await query.answer()
                        await query.edit_message_text(
                            message, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
                    else:
                        await query.answer(locales['no_updates'])
                else:
                    await query.answer()
        else:

            if len(followed_canteens) == 0:
                await query.answer()
                await query.edit_message_text(locales["favorites_empty"], reply_markup=InlineKeyboardMarkup(keyboard))
                return

            menus = []

            message = build_combined_message(followed_canteens, detailed)

            await query.answer()
            await query.edit_message_text(message, reply_markup=InlineKeyboardMarkup(keyboard))
