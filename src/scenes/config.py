from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import db.users as users
from helper.locales import locales


def build_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🛑", callback_data='config-stop'),
            InlineKeyboardButton("⚖️", callback_data='config-details'),
        ],
        [
            InlineKeyboardButton("◀️", callback_data='start'),
        ]
    ]

    return keyboard


async def scene(update: Update, context: ContextTypes.DEFAULT_TYPE, scene_data):
    query = update.callback_query

    if (query):
        user_id = query.from_user.id
        keyboard = build_keyboard()

        if (len(scene_data) > 0):
            command = scene_data[0]

            if (command == 'details'):
                if len(scene_data) >= 2:
                    if scene_data[1] == 'enable':
                        users.set_detailed(user_id, True)
                        await query.answer(locales['details_enabled'])
                    elif scene_data[1] == 'disable':
                        users.set_detailed(user_id, False)
                        await query.answer(locales['details_disabled'])

                    await query.answer("")
                    await query.edit_message_text(locales['config'], reply_markup=InlineKeyboardMarkup(keyboard))

                else:
                    keyboard = [
                        [
                            InlineKeyboardButton(
                                "❌", callback_data='config-details-disable'),
                            InlineKeyboardButton(
                                "✅", callback_data='config-details-enable'),
                        ],
                    ]

                    await query.edit_message_text(locales['details'], reply_markup=InlineKeyboardMarkup(keyboard))
                    await query.answer()

            elif command == 'stop':
                if (len(scene_data) == 2):
                    if scene_data[1] == 'confirm':
                        users.delete(user_id)
                        await query.answer()
                        await query.edit_message_text(locales['stop'], reply_markup=InlineKeyboardMarkup([]))

                else:
                    keyboard = [
                        [
                            InlineKeyboardButton(
                                "❌", callback_data='config'),
                            InlineKeyboardButton(
                                "✅", callback_data='config-stop-confirm'),
                        ],
                    ]

                    await query.answer()
                    await query.edit_message_text(locales["stop_confirm"], reply_markup=InlineKeyboardMarkup(keyboard))

        else:
            await query.answer("")
            await query.edit_message_text(locales['config'], reply_markup=InlineKeyboardMarkup(keyboard))
