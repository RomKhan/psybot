from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from ..util import ReplyMarkupType, load_data_file


class BaseState:
    message: str
    name: str
    buttons: list[list[str]] | None
    transitions: dict[str, str]

    def __init__(self) -> None:
        data = load_data_file("states", self.name)
        self.message = data["message"]
        self.buttons = data["buttons"]
        self.transitions = data["transitions"]

    def get_message(self) -> str:
        return self.message

    def get_buttons(self) -> ReplyMarkupType:
        if self.buttons is not None:
            return ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=e) for e in l] for l in self.buttons],
                resize_keyboard=True,
            )
        else:
            return ReplyKeyboardRemove()

    def next_state(self, text: str) -> str | None:
        return self.transitions.get(text.strip())
