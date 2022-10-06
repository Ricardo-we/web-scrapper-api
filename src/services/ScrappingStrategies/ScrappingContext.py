from .BaseStrategy import BaseStrategy
from .CemacoStrategy import CemacoStrategy
from .EpaStrategy import EpaStrategy
from .NovexStrategy import NovexStrategy


class ScrappingContext:
    valid_scrapping_names = ["cemaco", "epa", "novex"]
    strategy = CemacoStrategy()

    def __init__(self, scrapping_page_name="cemaco") -> None:
        self.set_strategy(scrapping_page_name)

    def set_strategy(self, scrapping_page_name: str) -> BaseStrategy:
        if not (scrapping_page_name in self.valid_scrapping_names):
            raise Exception("Invalid strategy name")
        if scrapping_page_name == "cemaco":
            self.strategy = CemacoStrategy()
        elif scrapping_page_name == "epa":
            self.strategy = EpaStrategy()
        elif scrapping_page_name == "novex":
            self.strategy = NovexStrategy()

        return self

    def execute(self, search=""):
        return self.strategy.format_page_data(search)
