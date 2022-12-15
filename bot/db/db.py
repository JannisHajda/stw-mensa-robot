import psycopg2
from helper.config import config
import db.canteens as canteens

class DB:

    def get_tables(self):
        cur = self.conn.cursor()
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        tables = cur.fetchall()
        cur.close()
        tables = [table[0] for table in tables]
        return tables

    def setup(self):
        cur = self.conn.cursor()

        if ("canteens" in self.get_tables()):
            return

        cur.execute("""CREATE TABLE IF NOT EXISTS canteens (
            id SERIAL PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            name VARCHAR(253),
            url VARCHAR(253), 
            menu json)""")
        
        # insert canteens
        canteens = [
            ('Brandenburg', "https://xml.stw-potsdam.de/xmldata/b/xml.php"),
            ('Kiepenheuerallee', "https://xml.stw-potsdam.de/xmldata/ka/xml.php"),
            ('Griebnitzsee', 'https://xml.stw-potsdam.de/xmldata/gs/xml.php'),
            ('Am Neuen Palais', 'https://xml.stw-potsdam.de/xmldata/np/xml.php'),
            ('Filmuniversität', 'https://xml.stw-potsdam.de/xmldata/fi/xml.php'),
            ('Golm', 'https://xml.stw-potsdam.de/xmldata/go/xml.php'),
            ('Wildau', 'https://xml.stw-potsdam.de/xmldata/w/xml.php')
        ]

        for canteen in canteens:
            cur.execute("INSERT INTO canteens (name, url, menu) VALUES (%s, %s, NULL)", canteen)

        cur.execute("""CREATE TABLE IF NOT EXISTS users (
            id bigint PRIMARY KEY, 
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            detailed BOOLEAN DEFAULT FALSE
        )""")

        cur.execute("""CREATE TABLE IF NOT EXISTS users_follow_canteens (
            user_id bigint REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
            canteen_id serial REFERENCES canteens(id) ON DELETE CASCADE ON UPDATE CASCADE, 
            push BOOLEAN DEFAULT FALSE
        )""")

        self.conn.commit()
        cur.close()

    def __init__(self):
        self.conn = psycopg2.connect("dbname=%s user=%s password=%s host=%s port=%s" % (
            config.env["POSTGRES_DB"], config.env["POSTGRES_USER"], config.env["POSTGRES_PASSWORD"], config.env["POSTGRES_HOST"], config.env["POSTGRES_PORT"]))
        if (self.conn):
            self.setup() 
            

db = DB()
