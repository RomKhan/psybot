from ..models import User
from .BaseState import BaseState


class ArticleState(BaseState):
    name = "Articles"

    def __init__(self, user: User, text: str) -> None:
        super().__init__(user, text)
        pass
