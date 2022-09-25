from sqlalchemy import select, insert, update, delete
from fastapi import APIRouter
from fastapi.responses import Response
# from .model import User, conn
from .context import UserContext
from src.utils.base.DefaultResponses import DefaultResponses
from src.services.ScrappingStrategies.ScrappingContext import ScrappingContext

route_name = "scrap"
scraps_router = APIRouter()
users_context = UserContext()


@scraps_router.get(f"/{route_name}")
def get_scrapped_page():
    try:
        scrapping_context = ScrappingContext()
        result = scrapping_context.execute()
        return result
    except Exception as err:
        return DefaultResponses.error_response(err, "Something went wrong")
