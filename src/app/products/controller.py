from sqlalchemy import select, insert, update, delete
from fastapi.responses import Response

from src.app.products.controllers.product_tags_context import ProductTagsContext
from .model import Product, ProductTag, conn
from src.utils.base.DefaultResponses import DefaultResponses
from src.services.ScrappingStrategies.ScrappingContext import ScrappingContext
from .controllers.product_tags import router

route_name = "scrap"


@router.get(f"/{route_name}")
def get_scrapped_page(search: str):
    try:
        result = conn.execute(select(Product).filter(Product.name.like(f"%{search}%"))).fetchall()
        return result
    except Exception as err:
        return DefaultResponses.error_response(err, "Something went wrong")


@router.put(f"/refresh-products")
def refresh():
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
