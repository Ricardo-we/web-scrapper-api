from src.services.WebDriver.WebDriver import WebDriver
from .BaseStrategy import BaseStrategy
from bs4 import BeautifulSoup


class CemacoStrategy(BaseStrategy):
    url = "https://www.cemaco.com"
    endpoint = ""

    def get_page_data(self):
        return super().get_page_data()

    def random_selection(self):
        page_data = self.get_page_data().text
        doc = BeautifulSoup(page_data, "html.parser")
        product_items = doc.find_all(class_="product-item")
        result = []
        for single_product in product_items:
            product_price = single_product.find("span", class_="price-new").string
            product_url = single_product.find("a").get("href")
            product_image = single_product.find("img").get("src")
            result.append({"price": product_price, "url": product_url, "img": product_image})

        return result

    def format_page_data(self, search):
        self.set_endpoint(f"/buscar?q={search}")
        webdriver = WebDriver.get_dynamic_page_content(self.url + self.endpoint)
        doc = BeautifulSoup(webdriver.page_source, "html.parser")
        product_items = doc.find_all(class_="product-item")
        result = []
        for single_product in product_items:
            product_info = {
                "price":  single_product.find("div", class_="old-product-price").string,
                "url":  single_product.find("a").get("href"),
                "description": single_product.find("div", class_=["flags", "ng-binding"]).string,
                "img": single_product.find("img").get("src"),
                "is_offer": single_product.find("div", class_="offer") != None
            }

            print(product_info)

            result.append(product_info)

        webdriver.quit()

        return result
