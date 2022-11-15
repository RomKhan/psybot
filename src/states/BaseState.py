from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from ..models import ActionLog, User
from ..util import ReplyMarkupType, load_data_file


class BaseState:
    name: str
    text: str
    user: User

    message: str
    buttons: list[list[str]] | None
    transitions: dict[str, str]

    def __init__(self, user: User, text: str) -> None:
        self.user = user
        self.text = text

        data = load_data_file("states", self.name)
        self.message = data["message"]
        self.buttons = data["buttons"]
        self.transitions = data["transitions"]

    def get_message(self) -> str:
        return self.message

    def get_buttons(self) -> ReplyMarkupType:
        if self.buttons is not None:
            return ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=e) for e in list] for list in self.buttons],
                resize_keyboard=True,
            )
        else:
            return ReplyKeyboardRemove()

    def next_state(self) -> str | None:
        return self.transitions.get(self.text)

    def log(self, next_name: str | None = None) -> ActionLog:
        if next_name is None:
            next_name = self.name

        return ActionLog(
            user_id=self.user.id,
            message_unix_time=self.user.message_unix_time,
            old_state_name=self.user.state_name,
            new_state_name=next_name,
        )
