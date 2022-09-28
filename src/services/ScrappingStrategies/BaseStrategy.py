import requests

from src.services.WebDriver.WebDriver import WebDriver


class BaseStrategy:
    url = ""
    endpoint = ""
    shop_name = ""

    def __init__(self) -> None:
        pass

    def create_product_info_dict(self, product_key, name, description, price, image, product_url, is_offer=False):
        return {
            "product_key": product_key,
            "name": name,
            "description": description,
            "price": price,
            "image": image,
            "shop_name": self.shop_name,
            "product_url":  product_url,
            "is_offer": is_offer,
        }

    def get_page_data(self):
        response = requests.get(self.url + self.endpoint)
        return response

    def get_dynamic_page_data(self):
        webdriver = WebDriver(self.url + self.endpoint)
        return webdriver

    def set_endpoint(self, endpoint_name=""):
        self.endpoint = endpoint_name
        return self

    def random_selection(self):
        pass

    def format_page_data(self, search: str):
        pass
