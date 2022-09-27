from typing import Union

from pydantic import BaseModel, EmailStr

from src.utils.base.BaseContext import BaseContext


class ProductSchema(BaseModel):
    product_key: str
    name: str
    description: str
    price: str
    tag_id: int

class ProductsContext(BaseContext):
    schema: ProductSchema
    
    def __init__(self):
        self.schema = ProductSchema
