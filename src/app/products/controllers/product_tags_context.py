from src.utils.base.BaseContext import BaseContext
from src.services.ScrappingStrategies.ScrappingContext import ScrappingContext
from pydantic import BaseModel
from ..model import conn, Product, ProductTagToProducts, ProductTag
from sqlalchemy.sql import insert, select, literal_column
from src.utils.generic.string_utils import word_ends_with, VOCALS

class ProductTagSchema(BaseModel):
    name: str


class ProductTagsRepositorie(BaseContext):
    schema: ProductTagSchema

    def __init__(self):
        self.schema = ProductTagSchema

    def format_tag_name(self, tag_name) -> str | None:
        product_tag_correct_name = tag_name
        if not word_ends_with(tag_name, VOCALS + ["s", "n", "z"]): return None
        if len(tag_name) > 20:
            product_tag_correct_name = product_tag_correct_name.strip().split(" ")[0]
        if word_ends_with(product_tag_correct_name,  ["d", "j", "r", "n", "l", "z"]):
            product_tag_correct_name += "e"
        if not product_tag_correct_name.endswith("s"):
            product_tag_correct_name += "s"
        return product_tag_correct_name

    def find_products_by_tagname_in_shop(self, tagname):
        epa_products = ScrappingContext("epa").execute(tagname)
        novex_products = ScrappingContext("novex").execute(tagname)
        cemaco_products = ScrappingContext("cemaco").execute(tagname)

        return epa_products + cemaco_products + novex_products

    def create_products_and_join_tags(self, products, product_tag_id=None):
        # INSERT NEW PRODUCTS
        conn.execute(
            insert(Product)
            .values(products)
            .prefix_with("IGNORE")
        )
        product_keys = map(
            lambda item: item["product_key"],
            products
        )

        new_products = conn.execute(
            select(Product)
                .where(Product.product_key.in_(product_keys))
        )\
            .fetchall()

        if not product_tag_id:
            return new_products

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

    def find_and_create_products_from_shop(self, product_or_tagname, product_tag_id=None):
        all_products = self.find_products_by_tagname_in_shop(product_or_tagname)
        self.create_products_and_join_tags(all_products, product_tag_id)

    def find_product_tag_by_name(self, product_tag_name):
        return conn.execute(select(ProductTag).where(ProductTag.name == product_tag_name)).fetchone()

    def find_or_create_tag(self, tag_name):
        product_tag_correct_name = self.format_tag_name(tag_name)
        if product_tag_correct_name == None: return None
        product_tag = self.find_product_tag_by_name(product_tag_correct_name)
        if product_tag == None:
            conn.execute(
                insert(ProductTag)
                    .prefix_with("IGNORE")
                    .values(name=product_tag_correct_name)
            )
            return self.find_product_tag_by_name(product_tag_correct_name)
        return product_tag
