from src.services.WebDriver.WebDriver import WebDriver
from .BaseStrategy import BaseStrategy

from .BaseStrategy import BaseStrategy

from .BaseStrategy import BaseStrategy
from bs4 import BeautifulSoup
import re
import time


class NovexStrategy(BaseStrategy):
    url = "https://www.novex.com.gt"
    endpoint = ""
    novex_url_regex = "^https\:\/\//www.novex.com.gt\/"
    shop_name = "novex"

    def get_item_key(self, item_url):
        return re.sub(r"^\/", "", item_url).replace(".html", "")

    def random_selection(self):
        return []

    def find_page_products(self, product_items):
        result = []
        for single_product in product_items:
            try:
                product_a_tag = single_product.find("a")
                product_url = self.url + product_a_tag.get("href")
                item_description_ul_tag = single_product.find("ul")
                description = " ".join(map(lambda item: item.string, item_description_ul_tag.find_all("li")
                                           ),) if item_description_ul_tag else ""

                product_info = self.create_product_info_dict(
                    product_key=self.get_item_key(product_url),
                    name=product_a_tag.get("title").strip(),
                    description=description,
                    price=float(single_product.find("div", class_="price").text.split(" ")[0].replace(",", "")),
                    image=single_product.select(".productCard__imgContainer img:first-child")[0].get("data-src"),
                    product_url=product_url,
                )

                result.append(product_info)
            except Exception as err:
                continue
        return result
        # S2 COOKIE

    def find_current_page_products_container(self, doc):
        products_container = doc.find_all(
            "div",
            class_="catalog__data"
        )[0]
        return products_container.find_all("div", class_="productCard")

    def format_page_data(self, search):
        current_page = 0
        sleep_time = 3.5
        all_product_items = []

        self.set_endpoint(f"/search?page={current_page}&term={search}&limit=4")
        webdriver = WebDriver.get_driver()
        webdriver.get(self.full_url)
        webdriver.add_cookie({"name": "S2", "value": "3"})
        webdriver.refresh()

        try:
            time.sleep(sleep_time)
            page_data = webdriver.page_source

            while True:
                current_page += 1
                self.set_endpoint(f"/search?page={current_page}&term={search}&limit=4")
                webdriver.get(self.full_url)
                time.sleep(sleep_time)

                page_data = webdriver.page_source
                doc = BeautifulSoup(page_data, "html.parser")
                product_items = self.find_current_page_products_container(doc)
                all_product_items += product_items

                if len(list(product_items)) < 80:
                    break

            webdriver.quit()
            formatted_product_list = self.find_page_products(all_product_items)

            return formatted_product_list
        except Exception as err:
            if len(webdriver.current_url) > 0:
                webdriver.quit()
            return []
