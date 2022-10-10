from email.policy import default
from settings import get_mysql_connection
from sqlalchemy import Float, Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from src.utils.generic.DbUtils import create_many_to_many_relation

conn, Base = get_mysql_connection()

ProductTagToProducts = create_many_to_many_relation(
    Base.metadata,
    "product_tags_to_products",
    "product_tag",
    "product"
)


class ProductTag(Base):
    __tablename__ = 'product_tag'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    # description = Column(String(300))
    product = relationship("Product", secondary=ProductTagToProducts, back_populates="product_tag")


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    product_key = Column(String(255), unique=True, nullable=False)
    name = Column(String(255))
    description = Column(String(500), nullable=True)
    price = Column(Float())
    image = Column(String(255))
    shop_name = Column(String(255))
    product_url = Column(String(255))
    currency_symbol = Column(String(5), default="Q")
    is_offer = Column(Boolean)
    product_tag = relationship("ProductTag", secondary=ProductTagToProducts, back_populates="product")


class ProductSearchLog(Base):
    __tablename__ = "product_search_log"

    id = Column(Integer, primary_key=True)
    search = Column(String(255))


# Base.metadata.drop_all(conn)
Base.metadata.create_all(conn)
