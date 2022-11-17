import json
import typing
from functools import lru_cache
from os.path import join

from aiogram.types import ForceReply, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove

from .environment import DATA_DIR

ReplyMarkupType = typing.Union[
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ForceReply,
    None,
]

oops_message = "Что-то пошло не так!🙄😱"


@lru_cache
def load_data_file(type: str, name: str) -> dict[str, typing.Any]:
    path = join(DATA_DIR, type, name + ".json")
    with open(path, "r") as f:
        return json.load(f)


def flatten(list: typing.Collection[typing.Collection]):
    return [item for sublist in list for item in sublist]
