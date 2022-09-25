import requests


class BaseStrategy:
    url = ""
    endpoint = ""

    def __init__(self) -> None:
        pass

    def get_page_data(self):
        response = requests.get(self.url)
        return response

    def format_page_data(self):
        pass
