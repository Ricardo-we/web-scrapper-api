from settings import get_mysql_connection
from sqlalchemy import Column, Integer, String

conn, Base = get_mysql_connection()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))


Base.metadata.create_all(conn)
