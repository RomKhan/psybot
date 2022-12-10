from .ArticleState import ArticleCategoryState, ArticleState
from .BaseState import BaseState
from .BookRecommendationState import BookRecommendationState
from .FactState import FactState
from .FilmRecommendationState import FilmRecommendationState
from .LikeableState import LikeableState
from .PageableState import PageableState
from .SeriesRecommendationState import SeriesRecommendationState
from .TechniqueState import TechniqueCategoryState, TechniqueState

__all__ = [
    "BaseState",
    "LikeableState",
    "PageableState",
    "FactState",
    "ArticleState",
    "BookRecommendationState",
    "SeriesRecommendationState",
    "FilmRecommendationState",
    "TechniqueCategoryState",
    "TechniqueState",
]


def make_state(name: str) -> type[BaseState]:
    return type(f"{name}State", (BaseState,), {"name": name})


states_by_name: dict[str, type[BaseState]] = {
    "Start": make_state("Start"),
    "NotImplemented": make_state("NotImplemented"),
    "Recommendations": make_state("Recommendations"),
    "Facts": FactState,
    "BookRecommendations": BookRecommendationState,
    "SeriesRecommendations": SeriesRecommendationState,
    "FilmRecommendations": FilmRecommendationState,
    "Articles": ArticleState,
    "ArticleCategory": ArticleCategoryState,
    "Techniques": TechniqueState,
    "TechniqueCategory": TechniqueCategoryState,
}
