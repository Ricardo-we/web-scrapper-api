from typing import Union

from pydantic import BaseModel, EmailStr
from sqlalchemy import select, or_, insert
from .model import Product, ProductSearchLog, conn

from src.utils.base.BaseContext import BaseContext
from .controllers.product_tags_context import ProductTagsContext


class ProductSchema(BaseModel):
    product_key: str
    name: str
    description: str
    price: str
    tag_id: int


class ProductsContext(BaseContext):
    schema: ProductSchema

    def __init__(self):
        self.schema = ProductSchema

    def product_search_query(self, search: str):
        word_separated_search = f'%{"%".join(search.split(" "))}%'

        return or_(
            Product.name.like(word_separated_search),
            Product.name.like(f"%{search[0:3]}%{search}%"),
            Product.description.like(word_separated_search),
        )

    def check_search_results(self, products: list, search: str, query, search_log):
        product_tag_context = ProductTagsContext()
        if len(products) <= 5 and not search_log:
            conn.execute(insert(ProductSearchLog).values({"search": search}))
            product_tag_context.find_and_create_products_from_shop(search.split(" ")[0])
            products = conn.execute(query).fetchall()
            return False
        return True


class ProductSearchLogContext:

    def __init__(self):
        pass

    def find_log_by_search(self, search: str):
        return conn.execute(
            select(ProductSearchLog)
            .where(ProductSearchLog.search == search)
        )\
            .fetchone()
