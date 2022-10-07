import re
from fastapi import APIRouter

from src.utils.generic.DbUtils import paginated_select, select_or_create
from .product_tags_context import ProductTagsContext
from sqlalchemy import insert, update, delete, select, join, or_
from sqlalchemy.orm import Session
from ..model import Product, ProductTag, ProductTagToProducts, conn
from src.utils.base.DefaultResponses import DefaultResponses
import settings

route_name = "product-tags"
router = APIRouter()
product_tag_context = ProductTagsContext()


@router.post(f"/{route_name}")
def create_tag(product_tag: product_tag_context.schema):
    try:
        # CREATE PRODUCT_TAG
        tag_name_correct_name = product_tag_context.format_tag_name(product_tag.name)
        conn.execute(insert(ProductTag, {"name": tag_name_correct_name}).prefix_with("IGNORE"))
        return{"name": tag_name_correct_name}
    except Exception as err:
        return DefaultResponses.error_response(err)


@router.get(f"/{route_name}")
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
            all_products = product_tag_context.find_products_by_tagname_in_shop(tag_name_correct_name)
            product_tag_context.create_products_and_join_tags(all_products, product_tag.id)

            products = conn.execute(filtered_by_tag_products_query).fetchall()

        return {"products": products, "tag": product_tag}
    except Exception as err:
        return DefaultResponses.error_response(err)
