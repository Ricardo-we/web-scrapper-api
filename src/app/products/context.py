from typing import Union

from pydantic import BaseModel, EmailStr
from sqlalchemy import select, or_, insert, literal_column
from .model import Product, ProductSearchLog, conn

from src.utils.base.BaseContext import BaseContext
from .controllers.product_tags_context import ProductTagsRepositorie


class ProductSchema(BaseModel):
    product_key: str
    name: str
    description: str
    price: str
    tag_id: int


class ProductsRepositorie(BaseContext):
    schema: ProductSchema
    product_tag_context: ProductTagsRepositorie

    def __init__(self):
        self.schema = ProductSchema
        self.product_tag_context = ProductTagsRepositorie()

    def product_search_query(self, search: str):
        word_separated_search = f'%{"%".join(search.split(" "))}%'

        return or_(
            Product.name.like(word_separated_search),
            Product.name.like(f"%{search[0:3]}%"),
            Product.description.like(word_separated_search),
        )

    def check_search_results(self, products: list, search: str, query, search_log):
        # product_tag = self.product_tag_context.find_or_create_tag(search)
        # and product_tag == None
        if len(products) <= 5 and search_log == None :
            self.product_tag_context.find_and_create_products_from_shop(search.split(" ")[0])
            products = conn.execute(query).fetchall()
            return False
        return True


class ProductSearchLogRepositorie:

    def __init__(self):
        pass

    def find_log_by_search(self, search: str):
        return conn.execute(
            select(ProductSearchLog)
            .where(ProductSearchLog.search == search)
        )\
            .fetchone()

    def find_or_create_log(self, search: str):
        search_log = self.find_log_by_search(search)
        if search_log == None:
            return conn.execute(
                insert(ProductSearchLog)
                  .values(search=search)
            )
