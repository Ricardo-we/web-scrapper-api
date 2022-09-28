from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.sql import select, insert
from settings import get_mysql_connection
import settings


def create_many_to_many_relation(metadata, association_name, left_table_name, right_table_name):
    column_suffix = "_id"
    return Table(
        association_name,
        metadata,
        Column(left_table_name + column_suffix, ForeignKey(left_table_name + ".id")),
        Column(right_table_name + column_suffix, ForeignKey(right_table_name + ".id")),
    )


def select_or_create(conn, table_obj, data, where):
    item = conn.execute(select(table_obj).where(where)).first()
    if not item:
        conn.execute(insert(table_obj, data))
    item = conn.execute(select(table_obj).where(where)).first()
    return item


def paginated_select(table_obj, page=0):
    print(page * settings.PAGINATION_SIZE)
    query = select(table_obj)\
        .limit(settings.PAGINATION_SIZE)\
        .offset(page * settings.PAGINATION_SIZE)
    return query
