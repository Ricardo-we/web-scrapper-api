from fastapi import APIRouter

from src.utils.generic.DbUtils import paginated_select, select_or_create
from .product_tags_context import ProductTagsContext
from sqlalchemy.sql import insert, update, delete, select, join
from sqlalchemy.orm import Session
from ..model import Product, ProductTag, ProductTagToProducts, conn
from src.utils.base.DefaultResponses import DefaultResponses
import settings

route_name = "product_tags"
router = APIRouter()
product_tag_context = ProductTagsContext()


@router.post(f"/{route_name}")
def create_tag(product_tag: product_tag_context.schema):
    # CREATE PRODUCT_TAG
    conn.execute(insert(ProductTag, product_tag.dict()))
    return product_tag.dict()


@router.get(f"/{route_name}")
def create_products_by_tag_name(tag_name: str, current_page: int = 0):
    try:
        # CREATE PRODUCT_TAG IF NOT EXISTS
        product_tag = select_or_create(conn, ProductTag, {"name": tag_name}, ProductTag.name == tag_name)

        def get_products_by_tag():
            filtered_by_tag_products = paginated_select(
                join(
                    ProductTagToProducts,
                    Product,
                    ProductTagToProducts.c.product_id == Product.id
                ),
                current_page
            )

            return conn.execute(filtered_by_tag_products).fetchall()

        products = get_products_by_tag()

        if len(products) <= 0:
            all_products = product_tag_context.find_products_by_tagname(tag_name)
            product_tag_context.create_products_and_join_tags(all_products, product_tag.id)

            products = get_products_by_tag()

        return {"products": products, "tag": product_tag, "result_size": len(products)}
    except Exception as err:
        return DefaultResponses.error_response(err)
