import string
from .SqlRepository import SqlRepository
from .BaseRepository import BaseRepository


class DbRepository:
    connection = BaseRepository()
    db_url = ""

    def __init__(self, db_type: str, db_url: str):
        self.connection
        self.db_url = db_url
        if db_type == "mongo":
            self.connection = BaseRepository()
            return None
        else:
            self.connection = SqlRepository()

    def get_connection(self):
        return self.connection.get_connection(self.db_url)

    def set_connection_and_dburl(self, connection: str, db_url: str):
        self.connection = connection
        self.db_url = db_url
        return self
