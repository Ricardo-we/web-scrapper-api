import re
from sqlalchemy import select, insert, update, delete, or_, func
from fastapi.responses import Response
from fastapi_utils.tasks import repeat_every

from src.app.products.controllers.product_tags_context import ProductTagsContext
from src.utils.generic.DbUtils import paginated_select, select_or_create
from .model import Product, ProductSearchLog, ProductTag, conn
from src.utils.base.DefaultResponses import DefaultResponses
from src.services.ScrappingStrategies.ScrappingContext import ScrappingContext
from .controllers.product_tags import router

route_name = "products"
seven_days_in_seconds = int(6.8 * 24 * 60 * 60)
product_tag_context = ProductTagsContext()


@router.get(f"/{route_name}")
def find_products(search: str = None, current_page: int = 0):
    try:
        if not search or len(search) <= 0:
            query = paginated_select(Product, current_page)\
                .filter(or_(Product.price < 150, Product.is_offer))\
                .order_by(func.rand(), Product.price)
            return conn.execute(query).fetchall()

        word_separated_search = f'%{"%".join(search.split(" "))}%'
        query = paginated_select(Product,   current_page)\
            .filter(or_(
                Product.name.like(word_separated_search),
                Product.name.like(f"%{search[0:3]}%{search}%"),
                Product.description.like(word_separated_search),
            ))\
            .order_by(Product.price.asc(), Product.name.asc())
        search_log = conn.execute(select(ProductSearchLog).where(ProductSearchLog.search == search)).fetchone()
        products = conn.execute(query).fetchall()

        if len(products) <= 5 and len(search) > 0 and not search_log:
            conn.execute(insert(ProductSearchLog).values({"search": search}))
            product_tag_context.find_and_create_products_from_shop(search.split(" ")[0])
            products = conn.execute(query).fetchall()

        return products

    except Exception as err:
        print(err)
        return DefaultResponses.error_response(err, "Something went wrong")


@router.on_event("startup")
@repeat_every(seconds=seven_days_in_seconds, wait_first=True)
def refresh_products_by_tagnames():
    try:
        product_tag_context = ProductTagsContext()
        conn.execute(delete(Product))
        all_tags = conn.execute(select(ProductTag)).fetchall()
        for tag in all_tags:
            all_products = product_tag_context.find_products_by_tagname_in_shop(tag.name)
            product_tag_context.create_products_and_join_tags(all_products, tag.id)

        return {"message": "success", "tags": len(all_tags)}

    except Exception as err:
        return DefaultResponses.error_response(err)
