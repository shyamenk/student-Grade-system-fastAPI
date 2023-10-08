import os

import aiomysql
from dotenv import load_dotenv

load_dotenv()


DATABASE_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "user": os.getenv("DB_USERNAME"),
    "password": os.getenv("DB_PASSWORD"),
    "db": os.getenv("DB_NAME"),
    "autocommit": True,
}


async def get_database_connection():
    connection = await aiomysql.connect(**DATABASE_CONFIG)
    return connection
