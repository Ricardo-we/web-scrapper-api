import sys
# sys.path.append("../..")
from src.config.data.product_tags import product_tags_data
from .model import ProductTag, conn
from sqlalchemy.sql import insert


def seed():
    formatted_products = []
    # for product_tag in product_tags_data:
    #     try:
    #         new_product_tag = ProductTag(**product_tag)
    #         formatted_products.append(new_product_tag)
    #     except Exception as err: 
    #         print(err)

    conn.execute(
        insert(ProductTag)
        .values(product_tags_data)
        .prefix_with("IGNORE")
    )

    # new_product_tag.name = product_tag["name"]
