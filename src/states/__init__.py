from .BaseState import BaseState
from .BookRecommendationState import BookRecommendationState
from .FactState import FactState

__all__ = ["BaseState", "FactState", "BookRecommendationState"]


def make_state(name: str):
    return type(f"{name}State", (BaseState,), {"name": name})


states_by_name: dict[str, type[BaseState]] = {
    "Start": make_state("Start"),
    "NotImplemented": make_state("NotImplemented"),
    "Recommendations": make_state("Recommendations"),
    "Facts": FactState,
    "BookRecommendations": BookRecommendationState,
}
