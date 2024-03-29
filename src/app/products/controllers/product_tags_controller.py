import re
from fastapi import APIRouter

from src.utils.generic.DbUtils import paginated_select, select_or_create
from .product_tags_context import ProductTagsRepositorie
from sqlalchemy import insert, update, delete, select, join, or_
from sqlalchemy.orm import Session
from ..model import Product, ProductTag, ProductTagToProducts, conn
from src.utils.base.DefaultResponses import DefaultResponses
import settings

route_name = "product-tags"
router = APIRouter()
product_tag_context = ProductTagsRepositorie()


@router.post(f"/{route_name}")
def create_tag(product_tag: product_tag_context.schema):
    try:
        # CREATE PRODUCT_TAG
        new_product_tag = product_tag_context.find_or_create_tag(product_tag.name)
        return {"name": new_product_tag.name}
    except Exception as err:
        return DefaultResponses.error_response(err, "Invalid tag name")


@router.get(f"/{route_name}/{{tag_name}}")
def find_or_create_products_by_tagname(tag_name: str, current_page: int = 0):
    try:
        # CREATE PRODUCT_TAG IF NOT EXISTS
        tag_name_correct_name = product_tag_context.format_tag_name(tag_name)

        product_tag = select_or_create(
            conn,
            ProductTag,
            {"name": tag_name_correct_name},
            ProductTag.name == tag_name_correct_name
        )
        filtered_by_tag_products_query = paginated_select(
            join(
                ProductTagToProducts,
                Product,
                ProductTagToProducts.c.product_id == Product.id
            ),
            current_page
        )\
            .where(or_(Product.name.like(f"%{tag_name}%"), ProductTagToProducts.c.product_tag_id == product_tag.id))\
            .order_by(Product.price.asc(), Product.name.asc())

        products = conn.execute(filtered_by_tag_products_query).fetchall()

        if (len(products) <= 0 and current_page <= 0):
            product_tag_context.find_and_create_products_from_shop(tag_name, product_tag.id)
            products = conn.execute(filtered_by_tag_products_query).fetchall()

        return {"products": products, "tag": product_tag}
    except Exception as err:
        return DefaultResponses.error_response(err)


@router.get(f"/{route_name}")
def get_all_tags():
    try:
        all_tags = select(ProductTag)
        return conn.execute(all_tags).fetchall()
    except Exception as err:
        return DefaultResponses.error_response(err)
