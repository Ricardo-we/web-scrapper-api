from sqlalchemy import select, insert, update, delete
from fastapi import APIRouter
from fastapi.responses import Response
from .model import User, conn
from .context import UserContext
from src.utils.generic.Encrypter import Encrypter
from src.utils.base.DefaultResponses import DefaultResponses

route_name = "users"
user_router = APIRouter()
users_context = UserContext()


@user_router.get(f"/{route_name}")
def get_users():
    try:
        users = conn.execute(select(User)).fetchall()
        return users
    except Exception as err:
        return DefaultResponses.error_response(err, "Something went wrong")


@user_router.post(f"/{route_name}")
def create_user(user: users_context.schema):
    try:

        user_data = {"username": user.username, "email": user.email}
        user_data["password"] = Encrypter.encrypt(user.password)
        new_user = conn.execute(insert(User, user_data))
        return new_user
    except Exception as err:
        return DefaultResponses.error_response(err, "Something went wrong")


@user_router.put(f"/{route_name}/{{user_id}}")
def update_user(user_id: int, user: users_context.schema, response: Response):
    try:
        user_data = {"username": user.username, "email": user.email}
        user_data["password"] = Encrypter.encrypt(user.password)
        conn.execute(
            update(User)
            .where(User.id == user_id)
            .values(user_data)
        )
        return user_data
    except Exception as err:
        response.status_code = 500
        return DefaultResponses.error_response(err, "Something went wrong")


@user_router.delete(f"/{route_name}/{{user_id}}")
def delete_user(user_id: int, response: Response):
    try:
        conn.execute(
            delete(User)
            .where(User.id == user_id)
        )
        response_message, status = DefaultResponses.success_message(status=204)
        response.status_code = status
        return response_message
    except Exception as err:
        response.status_code = 500
        return DefaultResponses.error_response(err, "Something went wrong")
