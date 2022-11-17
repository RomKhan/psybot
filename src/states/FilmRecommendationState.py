from ..util import load_data_file
from .PageableState import PageableState


class FilmRecommendationState(PageableState):
    name = "FilmRecommendations"
    random_button = "Случайный фильм"
    start_button = "Фильмы"

    items: list[tuple[str, str]]

    def get_items(self) -> list[tuple[str, str]]:
        return list(load_data_file("recommendations", "Films").items())

    def get_headline(self, book: tuple[str, str]) -> str:
        return book[0]

    def print_item(self) -> str:
        book = self.items[self.item_number]
        return f"Рекомендация фильма №{self.item_number+1}\n\n{book[0]}\n\n{book[1]}"
