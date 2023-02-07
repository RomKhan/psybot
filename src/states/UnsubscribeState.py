from .BaseState import BaseState


class UnsubscribeState(BaseState):
    name = "Unsubscribe"

    def next_state(self) -> str | None:
        res = super().next_state()
        if res:
            return res

        # todo: actually unsubscribe
        return self.name
