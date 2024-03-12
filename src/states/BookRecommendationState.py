from ..util import recommendations_by_category
from .PageableState import PageableState


class BookRecommendationState(PageableState):
    name = "BookRecommendations"
    random_button = "🎲 Случайная книга"
    start_button = "📖 Книги"

    items: list[tuple[str, str]]

    def get_items(self) -> list[tuple[str, str]]:
        return recommendations_by_category("Books")

    def get_headline(self, book: tuple[str, str]) -> str:
        return book[0]

    def print_item(self) -> str:
        book = self.items[self.item_number]
        return f"Рекомендация книги №{self.item_number+1}\n\n{book[0]}\n\n{book[1]}"

    def print_recommendation(self) -> str:
        return ""
