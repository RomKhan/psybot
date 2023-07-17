from functools import lru_cache
from typing import Collection

from ..database import session
from ..models import Technique
from ..util import ReplyMarkupType
from .ArticleState import ArticleCategoryState
from .CategoryState import Categorizable
from .LikeableState import LikeableState
from .RecommendationManager import RecommendationManager


@lru_cache
def list_techniques() -> list[tuple[int, str, str, bool]]:
    columns = [Technique.id, Technique.category, Technique.title, Technique.needs_subscription]
    return session.query(*columns).distinct().all()


@lru_cache
def list_categories() -> Collection[str]:
    return set(e[1] for e in list_techniques())


@lru_cache
def techniques_by_cat(category: str, subscription: bool = False) -> list[Categorizable]:
    return [
        Categorizable(id, cat, title, sub)
        for id, cat, title, sub in list_techniques()
        if cat == category and (subscription or not sub)
    ]


@lru_cache
def get_technique(id: int) -> Technique:
    return session.query(Technique).get(id)


class TechniqueCategoryState(ArticleCategoryState):
    name = "TechniqueCategory"
    random_button = "Случайная техника"
    item_name = "Техника"

    selected_article: Technique | None

    def print_recommendation(self) -> str:
        try:
            manager = RecommendationManager(self.selected_article.id, "Technique")
            return manager.get_message().replace("{{STATE}}", "ознакомления с техникой")
        except (Exception,):
            return ""

    def get_items(self) -> list[Categorizable]:
        return techniques_by_cat(self.category, self.user.is_subscribed())

    def get_article(self) -> Technique:
        return get_technique(self.items[self.item_number].id)

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
