from ..util import recommendations_by_category
from .PageableState import PageableState


class FilmRecommendationState(PageableState):
    name = "FilmRecommendations"
    random_button = "🎲 Случайный фильм"
    start_button = "🎬 Фильмы"

    items: list[tuple[str, str]]

    def get_items(self) -> list[tuple[str, str]]:
        return recommendations_by_category("Films")

    def get_headline(self, book: tuple[str, str]) -> str:
        return book[0]

    def print_item(self) -> str:
        book = self.items[self.item_number]
        return f"Рекомендация фильма №{self.item_number+1}\n\n{book[0]}\n\n{book[1]}"

    def print_recommendation(self) -> str:
        return ""
