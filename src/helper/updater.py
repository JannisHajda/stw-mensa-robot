import helper.scraper as scraper
import db.users as users_db
import db.canteens as canteens_db
import json
from helper.build_menu_message import build_message
from helper.config import config
from telegram.ext import Updater, CallbackContext
from datetime import datetime, time


def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else:  # crosses midnight
        return check_time >= begin_time or check_time <= end_time


TOKEN = config.env["TELEGRAM_TOKEN"]

if not TOKEN:
    raise ValueError("No token provided")


async def notify_user(context, user, message, detailed_message):
    user_id = user[0]
    push = user[1]
    detailed = users_db.get(user[0])[2]

    if push:
        if detailed:
            await context.bot.send_message(
                user_id, detailed_message, parse_mode="HTML")
        else:
            await context.bot.send_message(user_id, message, parse_mode="HTML")


async def update(context: CallbackContext):
    canteens = canteens_db.list()

    for canteen in canteens:
        canteen_id = canteen[0]
        canteen_name = canteen[2]
        canteen_url = canteen[3]
        canteen_menu = json.dumps(canteen[4], indent=4, sort_keys=True)

        try:
            menu = scraper.scrape(canteen_url)
            if menu is not None:
                menu_json = json.dumps(menu, indent=4, sort_keys=True)

                if canteen_menu != menu_json:
                    canteens_db.update_menu(canteen_id, menu_json)

                    message = build_message(canteen_name, menu)
                    detailed_message = build_message(canteen_name, menu, True)
                    users = users_db.get_by_canteen(canteen_id)

                    if is_time_between(time(9, 0), time(15, 0), datetime.now().time()):
                        for user in users:
                            await notify_user(context, user, message, detailed_message)
        except:
            continue
