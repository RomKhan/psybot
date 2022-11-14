from .BaseState import BaseState

__all__ = ["BaseState"]


def make_state(name: str):
    return type(f"{name}State", (BaseState,), {"name": name})


states_by_name: dict[str, type[BaseState]] = {
    "Start": make_state("Start"),
    "NotImplemented": make_state("NotImplemented"),
}
