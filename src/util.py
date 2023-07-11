import json
import typing
from functools import lru_cache
from os.path import join

from aiogram.types import ForceReply, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove

from .database import session
from .environment import DATA_DIR
from .models import Recommendation

ReplyMarkupType = typing.Union[
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ForceReply,
    None,
]

oops_message = "Что-то пошло не так!🙄😱"

messages = {"oops_message": "Что-то пошло не так!🙄😱", "wrong_input": "Такого варианта нет!😤"}

@lru_cache
def load_data_file(type: str, name: str) -> dict[str, typing.Any]:
    path = join(DATA_DIR, type, name + ".json")
    with open(path, "r") as f:
        return json.load(f)


def flatten(list: typing.Collection[typing.Collection]):
    return [item for sublist in list for item in sublist]


@lru_cache
def recommendations_by_category(category: str, subscription: bool = False) -> list[tuple[str, str]]:
    columns = [
        Recommendation.category,
        Recommendation.title,
        Recommendation.needs_subscription,
        Recommendation.content,
    ]
    arr = session.query(*columns).distinct().all()
    return [
        (title, content)
        for cat, title, sub, content in arr
        if cat == category and (subscription or not sub)
    ]
