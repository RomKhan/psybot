from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from ..models import ActionLog, User
from ..util import ReplyMarkupType, load_data_file


class BaseState:
    name: str
    text: str
    user: User

    message: str
    buttons: list[list[str]]
    transitions: dict[str, str]
    inline_buttons: bool
    one_time_keyboard: bool

    def __init__(self, user: User, text: str) -> None:
        self.user = user
        self.text = text.strip()

        data = load_data_file("states", self.name)
        self.message = data["message"]
        self.buttons = data["buttons"] or []
        self.transitions = data["transitions"]
        self.inline_buttons = data.get("inline_buttons", False)
        self.one_time_keyboard = data.get("one_time_keyboard", True)

    def get_message(self) -> str:
        return self.message

    def get_buttons(self) -> ReplyMarkupType:
        if not self.buttons:
            return ReplyKeyboardRemove()
        elif self.inline_buttons:
            return InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text=e, callback_data=e) for e in list]
                    for list in self.buttons
                ],
            )
        else:
            return ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=e) for e in list] for list in self.buttons],
                resize_keyboard=True,
                one_time_keyboard=self.one_time_keyboard,
            )

    def next_state(self) -> str | None:
        res = self.transitions.get(self.text)
        if res == "THIS":
            return self.name
        return res

    def log(self, next_name: str | None = None) -> ActionLog:
        if next_name is None:
            self.commit()
            next_name = self.name

        return ActionLog(
            user_id=self.user.id,
            message_unix_time=self.user.message_unix_time,
            old_state_name=self.user.state_name,
            new_state_name=next_name,
            button_text=self.text,
        )

    def commit(self) -> None:
        pass

    def set_substate(self, *args: str) -> None:
        print(
            f"\x1b[31mWARNING\x1b[0m: state {self.name} is not supposed to have extra args: {args}"
        )

    def action(self, action: str, pram: int) -> None:
        print(f"\x1b[31mWARNING\x1b[0m: unsupported action {action}:{pram} for state {self.name}")
