import time
from selenium.webdriver import Chrome

CHROME_DRIVER_PATH = "C:/Program Files/chromedriver"


class WebDriver:
    driver: Chrome

    def __init__(self, url: str):
        self.driver = Chrome(executable_path=CHROME_DRIVER_PATH)
        self.driver.get(url)
        # chrome_driver.quit()

    @staticmethod
    def get_driver():
        return Chrome(executable_path=CHROME_DRIVER_PATH)

    def doc_scroll_bottom(self, scroll_timeout=3):
        # SCROLL_PAUSE_TIME = 0.5
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(scroll_timeout)
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
