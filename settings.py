from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base, sessionmaker
import os

from src.db.DbRepository import DbRepository

load_dotenv()

MYSQL_URL = os.environ.get("MYSQL_URL")


def get_mysql_connection():
    return DbRepository("sql", MYSQL_URL).get_connection(), declarative_base()
