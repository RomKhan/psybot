import json
import typing
from functools import lru_cache
from os.path import join
import re

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

messages = {"oops_message": "Что-то пошло не так!🙄😱", "wrong_number": "Такого варианта нет!😤",
            "wrong_input": "Неверный формат ввода!"}


@lru_cache
def load_data_file(type: str, name: str) -> dict[str, typing.Any]:
    path = join(DATA_DIR, type, name + ".json")
    with open(path, "r") as f:
        return json.load(f)


def flatten(list: typing.Collection[typing.Collection]):
    return [item for sublist in list for item in sublist]

def markdown_fix(text):
    text = '\n' + text
    text = re.sub(r'(\\\n)', r'', text)
    text = re.sub(r'(_)', r' ', text)
    text = re.sub(r'(\*\*)', r'_', text)
    text = re.sub(r'\*(.*?)\*', r'_\1_', text)
    text = re.sub(r'([*].*(?=\n))', r'\1*', text)
    text = '\n'.join([x.replace('_', '') if x.count('_') % 2 == 1 else x for x in '_'.join(list(filter(None, text.split('*')))).split('\n')])
    text = re.sub(r'(#.*(?=\n))', r'\1*', text)
    text = text.replace('#', '*')
    text = '*'.join(list(filter(None, text.split('*'))))
    return text.strip()


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
