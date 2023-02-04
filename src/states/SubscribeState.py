from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from quizlib.util import generate_prodamus_link

from ..models import User
from ..util import ReplyMarkupType
from .BaseState import BaseState


class SubscribeState(BaseState):
    name = "Subscribe"

    is_subscribed: bool
    url: str | None = None
    button: InlineKeyboardButton | None = None

    def __init__(self, user: User, text: str) -> None:
        super().__init__(user, text)
        self.is_subscribed = user.is_subscribed()
        self.buttons = self.buttons[:]

        if self.is_subscribed:
            self.message = self.data["message2"]
            del self.buttons[0]
        else:
            self.url = generate_prodamus_link(user.id)  # type: ignore
            self.button = InlineKeyboardButton(text=self.buttons[0][1], url=self.url)

    def get_buttons(self) -> ReplyMarkupType:
        if self.button is None:
            return super().get_buttons()
        res = InlineKeyboardMarkup(row_width=2)
        logged_in = self.user.linked_user is not None
        first_button = self.buttons[logged_in][0]
        res.insert(InlineKeyboardButton(text=first_button, callback_data=first_button))
        res.insert(self.button)
        res.add(InlineKeyboardButton(text=self.buttons[2][0], callback_data=self.buttons[2][0]))
        return res

    def inactive_buttons(self) -> InlineKeyboardMarkup | None:
        if self.button:
            res = InlineKeyboardMarkup(row_width=1)
            res.add(self.button)
            return res
        else:
            return None

    def next_state(self) -> str | None:
        if self.text == "Выйти из аккаунта":
            self.user.linked_user = None
            return self.name

        return super().next_state()
