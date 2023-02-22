from abc import ABC, abstractmethod
from typing import Collection, Optional

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from ..database import Base as BaseModel
from ..models import User
from ..util import ReplyMarkupType, flatten
from .BaseState import BaseState


class LikeableState(ABC, BaseState):
    selected_item: Optional[BaseModel]
    substate: type[BaseState]

    @abstractmethod
    def list_categories(self) -> Collection[str]:
        pass

    @abstractmethod
    def get_item(self, id: int) -> BaseModel:
        pass

    def __init__(self, user: User, text: str) -> None:
        self.selected_item = None
        super().__init__(user, text)

        # todo: only truncate data
        categories = sorted(self.list_categories())
        truncated_categories = [cat[:32] for cat in categories]
        self.buttons = [[e] for e in truncated_categories] + [[flatten(self.buttons)[-1]]]

        self.transitions = self.transitions.copy()
        for cat, tr in zip(categories, truncated_categories):
            self.transitions[tr] = f"{self.substate.name}/{cat}"

    def action(self, action: str, pram: int) -> None:
        if action == "like":
            delta = 1
        elif action == "dislike":
            delta = -1
        else:
            return super().action(action, pram)

        item = self.get_item(pram)
        item.like(delta, self.user.id)
        self.message = ""
        self.selected_item = item

    def get_buttons(self) -> ReplyMarkupType:
        if self.selected_item:
            return self.likes_keyboard(self.selected_item)
        return super().get_buttons()

    @classmethod
    def likes_keyboard(cls, item: BaseModel) -> InlineKeyboardMarkup:
        name = cls.name
        id = item.id
        likes = item.likes
        dislikes = -likes if likes < 0 else ""
        likes = likes if likes > 0 else ""

        btn1 = InlineKeyboardButton(text=f"👍 {likes}", callback_data=f"{name}/like:{id}")
        btn2 = InlineKeyboardButton(text=f"👎 {dislikes}", callback_data=f"{name}/dislike:{id}")
        return InlineKeyboardMarkup(inline_keyboard=[[btn1, btn2]])
