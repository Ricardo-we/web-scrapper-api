from sqlalchemy import select, insert, update, delete
from fastapi.responses import Response
from .model import Product, ProductTag, conn
from src.utils.base.DefaultResponses import DefaultResponses
from src.services.ScrappingStrategies.ScrappingContext import ScrappingContext
from .controllers.product_tags import router

route_name = "scrap"


@router.get(f"/{route_name}")
def get_scrapped_page(search: str):
    try:
        # scrapping_context = ScrappingContext()
        # # if(len(search) > 0):
        # #     result = scrapping_context.execute(search)
        # # else:
        # #     result = scrapping_context.execute_random_selection()
        result = conn.execute(select(Product).filter(Product.name.like(f"%{search}%"))).fetchall()
        print(result)
        return result
    except Exception as err:
        return DefaultResponses.error_response(err, "Something went wrong")
