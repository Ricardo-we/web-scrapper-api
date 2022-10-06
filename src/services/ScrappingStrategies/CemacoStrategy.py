from src.utils.generic.string_utils import get_float_from_currency_format
from .BaseStrategy import BaseStrategy
from bs4 import BeautifulSoup
import re


class CemacoStrategy(BaseStrategy):
    url = "https://www.cemaco.com"
    endpoint = ""
    cemaco_url_regex = "^https\:\/\/www.cemaco.com\/"
    shop_name = "cemaco"

    def get_item_key(self, item_url):
        item_url_ref = item_url
        if(len(re.findall(self.cemaco_url_regex, item_url)) <= 0):
            item_url_ref = self.url + item_url_ref
        return re.sub(self.cemaco_url_regex, "", item_url)

    def get_page_data(self):
        return super().get_page_data()

    def random_selection(self):
        page_data = self.get_page_data().text
        doc = BeautifulSoup(page_data, "html.parser")
        product_items = doc.find_all(class_="product-item")
        result = []
        for single_product in product_items:
            product_a_tag = single_product.find("a")
            product_url = product_a_tag.get("href")

            product_info = self.create_product_info_dict(
                product_key=self.get_item_key(product_url),
                name=product_a_tag.string,
                description="",
                price=get_float_from_currency_format(single_product.find("div", class_="price-new").string),
                image=self.url + single_product.find("img").get("src"),
                product_url=product_url,
                is_offer=single_product.find("div", class_="product-item__discount-news") != None,
            )

            result.append(product_info)

        return result

    def format_page_data(self, search):
        self.set_endpoint(f"/buscar?q={search}")
        webdriver = self.get_dynamic_page_data()
        try:
            webdriver.doc_scroll_bottom(3)
            page_data = webdriver.driver.page_source
            doc = BeautifulSoup(page_data, "html.parser")
            product_items = doc.find_all(class_="product-item")
            result = []
            for single_product in product_items:
                product_url = self.url + single_product.find("a").get("href")
                product_info = self.create_product_info_dict(
                    product_key=self.get_item_key(product_url),
                    name=single_product.find("div", class_="product-title").string,
                    description=single_product.find("div", class_=["flags", "ng-binding"]).string,
                    price=get_float_from_currency_format(single_product.find("div", class_="old-product-price").string),
                    image=self.url + single_product.find("img").get("src"),
                    product_url=product_url,
                    is_offer=single_product.find("div", class_="offer") != None
                )

                result.append(product_info)
            webdriver.driver.quit()
            return result
        except Exception as err:
            if len(webdriver.driver.current_url) > 0:
                webdriver.driver.quit()
            return []
