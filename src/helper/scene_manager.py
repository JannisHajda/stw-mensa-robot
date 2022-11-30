from telegram import Update
from telegram.ext import ContextTypes

import db.users as users

from scenes.config import scene as config_scene
from scenes.start import scene as start_scene
from scenes.favorites import scene as favorites_scene
from scenes.search import scene as search_scene
from scenes.canteen import scene as caneteen_scene


async def scene_manager(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if (query):
        user_id = query.from_user.id

        users.create_if_not_exists(user_id)

        data = query.data.split('-')
        scene_name = data[0]
        scene_data = data[1:]

        if scene_name == 'config':
            await config_scene(update, context, scene_data)
        elif scene_name == 'start':
            await start_scene(update, context, scene_data)
        elif scene_name == 'favorites':
            await favorites_scene(update, context, scene_data)
        elif scene_name == 'search':
            await search_scene(update, context, scene_data)
        elif scene_name == 'canteen':
            await caneteen_scene(update, context, scene_data)
        else:
            await query.answer()
            await query.edit_message_text("Unknown scene: " + scene_name)
