from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from .BaseRepository import BaseRepository


class SqlRepository(BaseRepository):
    def get_connection(self, db_url: str) -> Engine:
        connection = create_engine(db_url, echo=True)
        return connection
