from .BaseStrategy import BaseStrategy


class CemacoStrategy(BaseStrategy):
    url = "https://www.cemaco.com/"

    def get_page_data(self):
        return super().get_page_data()

    def format_page_data(self):
        page_data = self.get_page_data()
        print(page_data.text)
        return page_data.text
