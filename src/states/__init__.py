from .BaseState import BaseState
from .FactState import FactState

__all__ = ["BaseState", "FactState"]


def make_state(name: str):
    return type(f"{name}State", (BaseState,), {"name": name})


states_by_name: dict[str, type[BaseState]] = {
    "Start": make_state("Start"),
    "NotImplemented": make_state("NotImplemented"),
    "Facts": FactState,
}
