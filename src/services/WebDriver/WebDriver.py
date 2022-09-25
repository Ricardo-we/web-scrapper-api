from bs4 import BeautifulSoup
from selenium.webdriver import Chrome


class WebDriver:
    @staticmethod
    def get_dynamic_page_content(url: str):
        chrome_driver = Chrome(executable_path="C:/Program Files/chromedriver")
        chrome_driver.get(url)
        # chrome_driver.quit()
        return chrome_driver
