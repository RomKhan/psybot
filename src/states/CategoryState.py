from dataclasses import dataclass

from ..models import User
from .PageableState import PageableState


@dataclass(order=True)
class Categorizable:
    id: int
    category: str
    title: str
    needs_subscription: bool = False


class CategoryState(PageableState):
    category: str
    start_button = ""
    is_random = False

    items: list[Categorizable]

    def get_headline(self, item: Categorizable) -> str:
        return item.title + (" 🟡" if item.needs_subscription else "")

    def __init__(self, user: User, text: str) -> None:
        self.category = ""
        super().__init__(user, text)

    def set_substate(self, *args: str) -> None:
        assert len(args) == 1
        self.start_button = self.category = args[0]
        self.name = f"{self.name}/{self.category}"
        self.reload_items()

    def get_message(self) -> str:
        return super().get_message().replace("{{CATEGORY}}", self.category)
