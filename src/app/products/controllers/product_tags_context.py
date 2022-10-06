from src.utils.base.BaseContext import BaseContext
from src.services.ScrappingStrategies.ScrappingContext import ScrappingContext
from pydantic import BaseModel
from ..model import conn, Product, ProductTagToProducts
from sqlalchemy.sql import insert, select


class ProductTagSchema(BaseModel):
    name: str
    shop_name: str


class ProductTagsContext(BaseContext):
    schema: ProductTagSchema

    def __init__(self):
        self.schema = ProductTagSchema

    def find_products_by_tagname_in_shop(self, tagname):
        novex_products = ScrappingContext("novex").execute(tagname)
        # cemaco_products = ScrappingContext("cemaco").execute(tagname)
        # epa_products = ScrappingContext("epa").execute(tagname)

        # return epa_products + cemaco_products + novex_products
        return novex_products

    def create_products_and_join_tags(self, products, product_tag_id):
        # INSERT NEW PRODUCTS
        conn.execute(
            insert(Product)
            .prefix_with("IGNORE")
            .values(products)
        )
        product_keys = map(
            lambda item: item["product_key"],
            products
        )

        new_products = conn.execute(select(Product).where(Product.product_key.in_(product_keys))).fetchall()

        product_ids = list(
            map(
                lambda item: {"product_tag_id": product_tag_id, "product_id": item.id},
                new_products
            )
        )

        conn.execute(
            insert(ProductTagToProducts)
            .prefix_with("IGNORE")
            .values(product_ids)
        )
        return new_products
