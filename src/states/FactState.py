from .RecommendationManager import RecommendationManager
from ..util import flatten, load_data_file
from .PageableState import PageableState


class FactState(PageableState):
    def print_recommendation(self) -> str:
        return ""

    name = "Facts"
    random_button = "Случайный факт"
    start_button = "Факты"

    def get_items(self) -> list[str]:
        return flatten(load_data_file("", "facts").values())

    def get_headline(self, fact: str) -> str:
        return fact.split("\n")[0].split(". ")[0]

    def print_item(self) -> str:
        self.recommendation_message = self.print_recommendation()
        self.need_recommendation = True
        return f"Факт №{self.item_number+1}\n\n{self.items[self.item_number]}"
