from time import time
from selenium.webdriver import Chrome


class WebDriver:
    @staticmethod
    def get_dynamic_page_content(url: str):
        chrome_driver = Chrome(executable_path="C:/Program Files/chromedriver")
        chrome_driver.get(url)
        # chrome_driver.quit()
        return chrome_driver

    @staticmethod
    def doc_scroll_bottom(driver, scroll_timeout):
        # SCROLL_PAUSE_TIME = 0.5

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(scroll_timeout)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
