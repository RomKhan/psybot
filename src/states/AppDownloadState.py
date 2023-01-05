from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from ..util import ReplyMarkupType
from .BaseState import BaseState


class AppDownloadState(BaseState):
    name = "AppDownload"

    def get_buttons(self) -> ReplyMarkupType:
        res = InlineKeyboardMarkup(row_width=1)
        res.add(InlineKeyboardButton(text="Скачать", url=self.buttons[0][0]))
        res.add(InlineKeyboardButton(text=self.buttons[1][0], callback_data=self.buttons[1][0]))
        return res

    def inactive_buttons(self) -> InlineKeyboardMarkup | None:
        res = InlineKeyboardMarkup(row_width=1)
        res.add(InlineKeyboardButton(text="Скачать", url=self.buttons[0][0]))
        return res
