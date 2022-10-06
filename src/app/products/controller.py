from sqlalchemy import select, insert, update, delete, or_
from fastapi.responses import Response

from src.app.products.controllers.product_tags_context import ProductTagsContext
from src.utils.generic.DbUtils import paginated_select
from .model import Product, ProductTag, conn
from src.utils.base.DefaultResponses import DefaultResponses
from src.services.ScrappingStrategies.ScrappingContext import ScrappingContext
from .controllers.product_tags import router

route_name = "products"


@router.get(f"/{route_name}")
def find_products(search: str = None, page: int = 0):
    try:
        if not search or len(search) <= 0:
            query = paginated_select(Product, page).filter(or_(Product.price < 150, Product.is_offer))
            return conn.execute(query).fetchall()
        query = paginated_select(Product, page).filter(Product.name.like(f"%{search}%"))
        result = conn.execute(query).fetchall()
        return result
    except Exception as err:
        return DefaultResponses.error_response(err, "Something went wrong")


@router.put(f"/{route_name}/refresh")
def refresh():
    try:
        product_tag_context = ProductTagsContext()
        conn.execute(delete(Product))
        all_tags = conn.execute(select(ProductTag)).fetchall()
        result = []
        for tag in all_tags:
            all_products = product_tag_context.find_products_by_tagname_in_shop(tag.name)
            # product_tag_context.create_products_and_join_tags(all_products, tag.id)
            result.append(all_products)

        return {"message": "success", "tags": len(all_tags), "products": all_products}

    except Exception as err:
        return DefaultResponses.error_response(err)
