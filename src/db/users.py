from db.db import db


def create_if_not_exists(user_id):
    if not get(user_id):
        create(user_id, False)


def list():
    cur = db.conn.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.close()
    return users


def get(user_id):
    cur = db.conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    return user


def get_by_canteen(canteen_id):
    cur = db.conn.cursor()
    cur.execute(
        "SELECT user_id, push FROM users_follow_canteens WHERE canteen_id = %s", (canteen_id,))
    users = cur.fetchall()
    cur.close()
    return users


def delete(user_id):
    cur = db.conn.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    db.conn.commit()
    cur.close()


def set_detailed(user_id, detailed):
    cur = db.conn.cursor()
    cur.execute("UPDATE users SET detailed = %s WHERE id = %s",
                (detailed, user_id))
    db.conn.commit()
    cur.close()


def create(user_id, detailed):
    cur = db.conn.cursor()
    cur.execute("INSERT INTO users (id, detailed) VALUES (%s, %s)",
                (user_id, detailed))
    db.conn.commit()
    cur.close()


def following(user_id):
    cur = db.conn.cursor()
    cur.execute(
        "SELECT canteen_id  FROM users_follow_canteens WHERE user_id = %s", (user_id,))
    following = cur.fetchall()
    cur.close()
    return following


def follow(user_id, canteen_id, push):
    cur = db.conn.cursor()
    cur.execute("INSERT INTO users_follow_canteens (user_id, canteen_id, push) VALUES (%s, %s, %s)",
                (user_id, canteen_id, push))
    db.conn.commit()
    cur.close()


def unfollow(user_id, canteen_id):
    cur = db.conn.cursor()
    cur.execute("DELETE FROM users_follow_canteens WHERE user_id = %s AND canteen_id = %s",
                (user_id, canteen_id))
    db.conn.commit()
    cur.close()


def enable_push(user_id, canteen_id):
    cur = db.conn.cursor()
    cur.execute("UPDATE users_follow_canteens SET push = TRUE WHERE user_id = %s AND canteen_id = %s",
                (user_id, canteen_id))
    db.conn.commit()
    cur.close()


def disable_push(user_id, canteen_id):
    cur = db.conn.cursor()
    cur.execute("UPDATE users_follow_canteens SET push = FALSE WHERE user_id = %s AND canteen_id = %s",
                (user_id, canteen_id))
    db.conn.commit()
    cur.close()


def following_canteen(user_id, canteen_id):
    cur = db.conn.cursor()
    cur.execute(
        "SELECT push FROM users_follow_canteens WHERE user_id = %s AND canteen_id = %s", (user_id, canteen_id))
    following = cur.fetchone()
    cur.close()
    return following
