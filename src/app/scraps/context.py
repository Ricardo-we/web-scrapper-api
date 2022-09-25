from typing import Union

from pydantic import BaseModel, EmailStr

from src.utils.base.BaseContext import BaseContext


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserContext(BaseContext):

    schema: UserSchema

    def __init__(self):
        self.schema = UserSchema
