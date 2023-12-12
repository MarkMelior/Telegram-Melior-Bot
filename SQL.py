import psycopg2



# LOCALHOST SQL
HOST = '127.0.0.1'
USER = 'postgres'
PASSWORD = ''
DB_NAME = 'telegram'
PORT = 5432
connection = psycopg2.connect(
    host = HOST,
    port = PORT,
    user = USER,
    password = PASSWORD,
    database = DB_NAME
)


# from cogs.config import load_config
# config = load_config(".env")
# import urllib.parse as up
# up.uses_netloc.append("postgres")
# connection = psycopg2.connect(f"dbname='{config.db.database}' user='{config.db.user}' host='{config.db.host}' password='{config.db.password}'")


cursor = connection.cursor()


def sub_exists(user_id):
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
    return bool(len(cursor.fetchall()))

def close():
    connection.close()