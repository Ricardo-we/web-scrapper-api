from .BaseStrategy import BaseStrategy

from src.services.WebDriver.WebDriver import WebDriver
from .BaseStrategy import BaseStrategy
from bs4 import BeautifulSoup
import re


class EpaStrategy(BaseStrategy):
    url = "https://gt.epaenlinea.com/"
    endpoint = ""
    cemaco_url_regex = "^https\:\/\/gt.epaenlinea.com\/"
    shop_name = "epa"

    def get_item_key(self, item_url):
        item_url_ref = item_url
        if(len(re.findall(self.cemaco_url_regex, item_url)) <= 0):
            item_url_ref = self.url + item_url_ref
        return re.sub(self.cemaco_url_regex, "", item_url).replace(".html", "")

    def get_page_data(self):
        return super().get_page_data()

    def random_selection(self):
        page_data = self.get_page_data().text
        doc = BeautifulSoup(page_data, "html.parser")
        product_items = doc.find_all(class_="product-item")
        result = []
        for single_product in product_items:
            product_url = single_product.find("a").get("href")
            product_info = {
                "price":  single_product.find("div", class_="price-new").string,
                "product_url":  product_url,
                "image": self.url + single_product.find("img").get("src"),
                "product_key": self.get_item_key(product_url),
                # "description": single_product.find("div", class_=["flags", "ng-binding"]).string,
                "is_offer": single_product.find("div", class_="offer") != None
            }
            result.append(product_info)

        return result

    def format_page_data(self, search):
        self.set_endpoint(f"catalogsearch/result/index/?q={search}")
        page_data = self.get_page_data().text
        doc = BeautifulSoup(page_data, "html.parser")
        product_items = doc.find_all(class_="product-item-info")
        result = []
        for single_product in product_items:
            product_url = single_product.find("a").get("href")
            product_info = self.create_product_info_dict(
                product_key=self.get_item_key(product_url),
                name=single_product.find(class_="product-item-link").string.strip(),
                description="",
                price=single_product.find("span", class_="price-wrapper").get("data-price-amount"),
                image=single_product.find("img").get("src"),
                product_url=product_url,
                is_offer=single_product.find("div", class_="offer") != None
            )

            result.append(product_info)

        return result
