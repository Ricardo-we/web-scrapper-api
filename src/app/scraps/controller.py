from sqlalchemy import select, insert, update, delete
from fastapi import APIRouter
from fastapi.responses import Response
# from .model import User, conn
from .context import UserContext
from src.utils.base.DefaultResponses import DefaultResponses
from src.services.ScrappingStrategies.ScrappingContext import ScrappingContext

route_name = "scrap"
router = APIRouter()
users_context = UserContext()


@router.get(f"/{route_name}")
def get_scrapped_page(search: str):
    try:
        scrapping_context = ScrappingContext()
        if(len(search) > 0):
            result = scrapping_context.execute(search)
        else:
            result = scrapping_context.execute_random_selection()
        return result
    except Exception as err:
        return DefaultResponses.error_response(err, "Something went wrong")
