from abc import ABC
from quizlib.models import Lesson
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from functools import lru_cache
from typing import Collection

from ..util import ReplyMarkupType
from ..database import session
from ..models import User, Course
from .CourseState import CourseState
from .LikeableState import LikeableState


@lru_cache
def get_lesson(id: int) -> Lesson:
    return session.query(Lesson).get(id)

@lru_cache
def list_courses() -> list[tuple[int, str, bool]]:
    columns = [Course.id, Course.name, Course.needs_subscription]
    return session.query(*columns).distinct().all()



@lru_cache
def list_courses_name() -> list[str]:
    return [x[1] for x in list_courses()]


class ChooseCourseState(LikeableState, ABC):
    name = "Courses"
    substate = CourseState

    def __init__(self, user: User, text: str) -> None:
        super().__init__(user, text)

    def list_courses(self) -> list[str]:
        return list_courses_name()

    def list_categories(self) -> Collection[str]:
        return self.list_courses()

    def get_item(self, id: int) -> Lesson:
        return get_lesson(id)

    def get_buttons(self) -> ReplyMarkupType:
        res = InlineKeyboardMarkup(row_width=1)
        for course in self.list_courses():
            res.insert(InlineKeyboardButton(text=course, callback_data=course))
        res.add(InlineKeyboardButton(text=self.buttons[-1][0], callback_data=self.buttons[-1][0]))
        return res
