from src.services.WebDriver.WebDriver import WebDriver
from .BaseStrategy import BaseStrategy

from .BaseStrategy import BaseStrategy

from .BaseStrategy import BaseStrategy
from bs4 import BeautifulSoup
import re
import time


class NovexStrategy(BaseStrategy):
    url = "https://www.novex.com.gt/"
    endpoint = ""
    novex_url_regex = "^https\:\/\//www.novex.com.gt\/"
    shop_name = "novex"

    def get_item_key(self, item_url):
        return re.sub(r"^\/", "", item_url).replace(".html", "")

    def random_selection(self):
        # page_data = self.get_page_data().text
        # doc = BeautifulSoup(page_data, "html.parser")
        # product_items = doc.find_all(class_="product-item")
        # result = []
        # for single_product in product_items:
        #     product_url = single_product.find("a").get("href")
        #     product_info = {
        #         "price":  single_product.find("div", class_="price-new").string,
        #         "product_url":  product_url,
        #         "image": self.url + single_product.find("img").get("src"),
        #         "product_key": self.get_item_key(product_url),
        #         # "description": single_product.find("div", class_=["flags", "ng-binding"]).string,
        #         "is_offer": single_product.find("div", class_="offer") != None
        #     }
        #     result.append(product_info)

        return []

    def find_page_products(self, product_items):
        result = []
        for single_product in product_items:
            product_a_tag = single_product.find("a")
            product_url = product_a_tag.get("href")
            description = map(lambda item: item.string, single_product.find("ul").find_all("li"))

            product_info = self.create_product_info_dict(
                product_key=self.get_item_key(product_url),
                name=product_a_tag.get("title").strip(),
                description="".join(description),
                price=single_product.find("div", class_="price").string,
                image=single_product.find("img").get("src"),
                product_url=product_url,
            )

            result.append(product_info)
        return result
        # S2 COOKIE

    def page_has_next(self, doc):
        return doc\
            .find("div", class_="paginator-container")\
            .find_all("a", class_="paginate__item")[1]\
            .get("style") == None

    def format_page_data(self, search):
        current_page = 1
        sleep_time = 4
        all_product_items = []

        self.set_endpoint(f"search?page={current_page}&term={search}&limit=4")
        webdriver = WebDriver.get_driver()
        webdriver.get(self.full_url)
        webdriver.add_cookie({"name": "S2", "value": "3"})
        webdriver.refresh()

        try:
            time.sleep(sleep_time)
            page_data = webdriver.page_source
            doc = BeautifulSoup(page_data, "html.parser")
            has_next = self.page_has_next(doc)
            # print("HAS NEXT: ", has_next)
            # print(doc.find("a", class_="paginate__item", text=re.compile(r".*SIGUIENTE.*")))

            while has_next:
                current_page += 1
                self.set_endpoint(f"search?page={current_page}&term={search}&limit=4")

                webdriver.get(self.full_url)
                time.sleep(sleep_time)
                page_data = webdriver.page_source
                doc = BeautifulSoup(page_data, "html.parser")
                product_items = doc.find("div", class_="catalog__data").find("div").children
                print(product_items)
                print(len(product_items))
                all_product_items.append(product_items)
                # has_next = self.page_has_next(doc)

                if len(product_items <= 0):
                    break

            webdriver.quit()
            result = []

            for product_items in all_product_items:
                result += self.find_page_products(product_items)

            return result
        except Exception as err:
            if len(webdriver.current_url) > 0:
                webdriver.quit()
            return []
