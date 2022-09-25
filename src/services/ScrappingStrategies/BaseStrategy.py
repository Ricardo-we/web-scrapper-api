import requests


class BaseStrategy:
    url = ""
    endpoint = ""

    def __init__(self) -> None:
        pass

    def get_page_data(self):
        response = requests.get(self.url + self.endpoint)
        return response

    def set_endpoint(self, endpoint_name=""):
        self.endpoint = endpoint_name
        return self

    def random_selection(self):
        pass

    def format_page_data(self, search: str):
        pass
