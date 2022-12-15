from db.db import db

def list():
    cur = db.conn.cursor()
    cur.execute("SELECT * FROM canteens")
    canteens = cur.fetchall()
    cur.close()
    return canteens
    

def get(id):
    cur = db.conn.cursor()
    cur.execute("SELECT * FROM canteens WHERE id = %s", (id,))
    canteen = cur.fetchone()
    cur.close()
    return canteen


def get_by_name(name):
    cur = db.conn.cursor()
    cur.execute("SELECT * FROM canteens WHERE name = %s", (name,))
    canteen = cur.fetchone()
    cur.close()
    return canteen


def delete(id):
    cur = db.conn.cursor()
    cur.execute("DELETE FROM canteens WHERE id = %s", (id,))
    db.conn.commit()
    cur.close()


def get_menu(id):
    cur = db.conn.cursor()
    cur.execute("SELECT menu FROM canteens WHERE id = %s", (id,))
    menu = cur.fetchone()
    cur.close()
    return menu


def update_menu(id, menu):
    cur = db.conn.cursor()
    cur.execute("UPDATE canteens SET menu = %s WHERE id = %s", (menu, id))
    db.conn.commit()
    cur.close()
