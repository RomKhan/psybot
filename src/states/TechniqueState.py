from functools import lru_cache
from typing import Collection

from ..database import session
from ..models import Technique
from ..util import ReplyMarkupType
from .ArticleState import ArticleCategoryState
from .LikeableState import LikeableState


@lru_cache
def list_techniques() -> list[tuple[int, str, str, bool]]:
    columns = [Technique.id, Technique.category, Technique.title, Technique.needs_subscription]
    return session.query(*columns).distinct().all()


@lru_cache
def list_categories() -> Collection[str]:
    return set(e[1] for e in list_techniques())


@lru_cache
def articles_by_cat(category: str, subscription: bool = False) -> list[tuple[int, str]]:
    return [
        (id, title)
        for id, cat, title, sub in list_techniques()
        if cat == category and (subscription or not sub)
    ]


@lru_cache
def get_technique(id: int) -> Technique:
    return session.query(Technique).get(id)


class TechniqueCategoryState(ArticleCategoryState):
    name = "TechniqueCategory"
    random_button = "Случайная техника"
    start_button = ""
    is_random = False
    item_name = "Техника"

    selected_article: Technique | None

    def get_items(self) -> list[tuple[int, str]]:
        return articles_by_cat(self.category, self.user.is_subscribed())

    def get_article(self) -> Technique:
        return get_technique(self.items[self.item_number][0])

    def get_buttons(self) -> ReplyMarkupType:
        # todo: use both keyboards
        if self.selected_article:
            return TechniqueState.likes_keyboard(self.selected_article)
        return super().get_buttons()


class TechniqueState(LikeableState):
    name = "Techniques"
    substate = TechniqueCategoryState

    def list_categories(self) -> Collection[str]:
        return list_categories()

    def get_item(self, id: int) -> Technique:
        return get_technique(id)
