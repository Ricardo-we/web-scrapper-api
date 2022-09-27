from fastapi import APIRouter
from .product_tags_context import ProductTagsContext
from sqlalchemy.sql import insert, update, delete
from ..model import Product, ProductTag, conn
from src.utils.base.DefaultResponses import DefaultResponses

route_name = "product_tags"
router = APIRouter()
product_tag_context = ProductTagsContext()


@router.post(f"/{route_name}")
def create_tag(product_tag: product_tag_context.schema):
    # CREATE PRODUCT_TAG
    conn.execute(insert(ProductTag, product_tag.dict()))
    return product_tag.dict()


@router.get(f"/{route_name}")
def create_products_by_tag_name(tag_name: str):
    try:

        # CREATE PRODUCT_TAG
        # conn.execute(insert(ProductTag, product_tag.dict()))
        cemaco_products = product_tag_context.find_products_by_tagname(tag_name)
        conn.execute(insert(Product).values(cemaco_products))
        return cemaco_products
    except Exception as err:
        return DefaultResponses.error_response(err)
