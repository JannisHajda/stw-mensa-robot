import psycopg2
from helper.config import config


class DB:
    def __init__(self):
        self.conn = psycopg2.connect("dbname=%s user=%s password=%s host=%s port=%s" % (
            config.env["POSTGRES_DB"], config.env["POSTGRES_USER"], config.env["POSTGRES_PASSWORD"], config.env["POSTGRES_HOST"], config.env["POSTGRES_PORT"]))


db = DB()
