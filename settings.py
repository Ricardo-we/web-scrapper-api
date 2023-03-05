from importlib import import_module
from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base, sessionmaker
import os

from src.db.DbRepository import DbRepository

load_dotenv()

MYSQL_URL = os.environ.get("MYSQL_URL")
TESTS = ["users"]
APPS = ["users", "products"]
PAGINATION_SIZE = 45
APP_ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

def load_apps(apps=[]):
    loaded_app_modules = []
    for app_name in apps:
        loaded_app_modules.append(import_module(f"src.app.{app_name}.controller").router)
    return loaded_app_modules


def get_mysql_connection():
    return DbRepository("sql", MYSQL_URL).get_connection(), declarative_base()
