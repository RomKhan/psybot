from ..models import User
from .BaseState import BaseState
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ..util import ReplyMarkupType


class ChooseCourseState(BaseState):
    name = "Courses"

    def __init__(self, user: User, text: str) -> None:
        super().__init__(user, text)

    def get_buttons(self) -> ReplyMarkupType:
        res = InlineKeyboardMarkup(row_width=1)
        res.add(InlineKeyboardButton(text=self.buttons[1][0], callback_data=self.buttons[1][0]))
        return res

    def get_message(self) -> str:
        return "КУРСЫ"