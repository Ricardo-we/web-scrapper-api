from sqlalchemy import Table, Column, Integer, String, ForeignKey


def create_many_to_many_relation(metadata, association_name, left_table_name, right_table_name):
    column_suffix = "_id"
    return Table(
        association_name,
        metadata,
        Column(left_table_name + column_suffix, ForeignKey(left_table_name + ".id")),
        Column(right_table_name + column_suffix, ForeignKey(right_table_name + ".id")),
    )
