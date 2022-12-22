import time
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from os import path

# CHROME_DRIVER_PATH = "C:/Program Files/chromedriver"
# CHROME_DRIVER_PATH = path.join("C:", "Program Files", "chromedriver") 

class WebDriver:
    driver: Chrome

    def __init__(self, url: str):
        self.driver = self.get_driver()
        self.driver.get(url)

    @staticmethod
    def get_driver():
        return Chrome(ChromeDriverManager().install())

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
