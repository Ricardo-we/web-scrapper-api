from src.utils.base.BaseContext import BaseContext
from src.services.ScrappingStrategies.ScrappingContext import ScrappingContext
from pydantic import BaseModel


class ProductTagSchema(BaseModel):
    name: str
    shop_name: str


class ProductTagsContext(BaseContext):
    schema: ProductTagSchema

    def __init__(self):
        self.schema = ProductTagSchema

    def find_products_by_tagname(self, tagname):
        cemaco_strategy = ScrappingContext("cemaco")
        # novex_strategy  = ScrappingContext("novex")
        # epa_strategy  = ScrappingContext("epa")
        cemaco_products = cemaco_strategy.execute(tagname)
        return cemaco_products
