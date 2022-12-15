from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import db.canteens as canteens
import db.users as users
from helper.locales import locales
from helper.build_menu_message import build_message


def build_keyboard(canteen_id, following, push):
    keyboard = [
        [
            InlineKeyboardButton(
                "💔" if following else "❤️",
                callback_data='canteen-' + str(canteen_id) + '-unfollow' if following else 'canteen-' + str(canteen_id) + '-follow'),
            InlineKeyboardButton(
                "🔕" if push else "🔔",
                callback_data='canteen-' + str(canteen_id) + '-push-disable' if push else 'canteen-' + str(canteen_id) + '-push-enable'),
            InlineKeyboardButton(
                "🔄", callback_data='canteen-' + str(canteen_id) + '-refresh'),
        ],
        [
            InlineKeyboardButton("◀️", callback_data='search'),
        ]
    ]

    return keyboard


async def scene(update: Update, context: ContextTypes.DEFAULT_TYPE, scene_data):
    query = update.callback_query

    if (query):
        user_id = query.from_user.id
        user = users.get(user_id)
        detailed = user[2]
        canteen_id = scene_data[0]

        canteen = canteens.get(canteen_id)
        canteen_name = canteen[2]
        canteen_menu = canteen[4]

        following = push = False
        join = users.following_canteen(user_id, canteen_id)

        message = build_message(canteen_name, canteen_menu, detailed)

        if join:
            following = True
            push = join[0]

        if len(scene_data) >= 2:
            command = scene_data[1]

            if command == 'refresh':

                if message.split() != query.message.text.split():
                    keyboard = build_keyboard(canteen_id, following, push)
                    await query.answer()
                    await query.edit_message_text(
                        text=message, reply_markup=InlineKeyboardMarkup(keyboard))
                else:
                    await query.answer(locales['no_updates'])

            elif command == 'push':
                if (len(scene_data) == 3):
                    if scene_data[2] == 'enable':
                        if not following:
                            users.follow(user_id, canteen_id, True)
                            following = True

                        users.enable_push(user_id, canteen_id)
                        push = True

                        keyboard = build_keyboard(canteen_id, following, push)
                        await query.answer(locales['push_enabled'])
                        await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))

                    elif scene_data[2] == 'disable':
                        users.disable_push(user_id, canteen_id)
                        push = False

                        keyboard = build_keyboard(canteen_id, following, push)
                        await query.answer(locales['push_disabled'])
                        await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))

            elif command == 'follow':
                users.follow(user_id, canteen_id, False)
                following = True

                keyboard = build_keyboard(canteen_id, following, push)
                await query.answer(locales['followed'])
                await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))

            elif command == 'unfollow':
                users.unfollow(user_id, canteen_id)
                following = False
                push = False

                keyboard = build_keyboard(canteen_id, following, push)
                await query.answer(locales['unfollowed'])
                await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            keyboard = build_keyboard(canteen_id, following, push)
            await query.answer()
            await query.edit_message_text(message, reply_markup=InlineKeyboardMarkup(keyboard))
