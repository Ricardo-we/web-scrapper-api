import re
from sqlalchemy import select, insert, update, delete, or_, func
from fastapi.responses import Response
from fastapi_utils.tasks import repeat_every

from src.app.products.controllers.product_tags_context import ProductTagsContext
from src.utils.generic.DbUtils import paginated_select, select_or_create
from .model import Product, ProductSearchLog, ProductTag, conn
from src.utils.base.DefaultResponses import DefaultResponses
from .controllers.product_tags_controller import router
from .context import ProductsContext, ProductSearchLogContext
from ...services.ScrappingStrategies.ScrappingContext import ScrappingContext

route_name = "products"
seven_days_in_seconds = int(6.8 * 24 * 60 * 60)
product_tag_context = ProductTagsContext()
products_context = ProductsContext()
products_log_context = ProductSearchLogContext()

@router.get(f"/{route_name}")
def find_products(search: str = None, current_page: int = 0):
    try:
        if not search or len(search) <= 0:
            query = paginated_select(Product, current_page)\
                .filter(or_(Product.price < 150, Product.is_offer))\
                .order_by(func.rand(), Product.price)
            return conn.execute(query).fetchall()

        product_search_query = products_context.product_search_query(search)
        query = paginated_select(Product, current_page)\
            .filter(product_search_query)\
            .order_by(Product.price.asc(), Product.name.asc())
        search_log = products_log_context.find_or_create_log(search)
        products = conn.execute(query).fetchall()
        products_context.check_search_results(products, search, query, search_log)

        return products

    except Exception as err:
        return DefaultResponses.error_response(err, "Something went wrong")

@router.get("/test-strategie/{strategie_name}")
def test_strategie(strategie_name: str, search: str):
    scrapping_context = ScrappingContext(strategie_name)
    return scrapping_context.execute(search)

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
