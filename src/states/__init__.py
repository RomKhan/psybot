from .ArticleState import ArticleState
from .BaseState import BaseState
from .BookRecommendationState import BookRecommendationState
from .FactState import FactState
from .FilmRecommendationState import FilmRecommendationState
from .SeriesRecommendationState import SeriesRecommendationState

__all__ = [
    "BaseState",
    "FactState",
    "ArticleState",
    "BookRecommendationState",
    "SeriesRecommendationState",
    "FilmRecommendationState",
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
}
