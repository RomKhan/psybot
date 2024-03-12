from datetime import timedelta

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from quizlib.api import generate_prodamus_link
from sqlalchemy import desc

from ..database import session
from ..models import Order, User
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
        else:
            email = ""
            if user.linked_user:
                email = user.linked_user.email
            self.url = generate_prodamus_link(user.id, email)  # type: ignore
            self.button = InlineKeyboardButton(text=self.buttons[0][1], url=self.url)

    # todo: пофиксить после добавления функционала на сервер
    def get_message(self) -> str:
        if self.is_subscribed:
            cond = Order.user_id == self.user.id
            if self.user.linked_user:
                cond |= Order.user_id == self.user.linked_user.id
            cond &= Order.last_updated != None  # noqa: E711
            order = session.query(Order).filter(cond).order_by(desc(Order.last_updated)).first()
            date = order.last_updated + timedelta(days=30)

            return self.message + f"\n\nДата следующей оплаты: {date}"

        return super().get_message()

    def get_buttons(self) -> ReplyMarkupType:
        res = InlineKeyboardMarkup(row_width=2)
        logged_in = self.user.linked_user is not None
        first_button = self.buttons[logged_in][0]
        res.insert(InlineKeyboardButton(text=first_button, callback_data=first_button))
        if self.button:
            res.insert(self.button)
        else:
            txt = self.buttons[1][1]
            res.insert(InlineKeyboardButton(text=txt, callback_data=txt))
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
        if self.text == self.buttons[1][0]:
            self.user.linked_user = None
            return self.name

        return super().next_state()
