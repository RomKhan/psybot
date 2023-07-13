from functools import lru_cache

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from quizlib.api import grade_quiz
from quizlib.models import Lesson
from typing import Collection

from ..database import session
from ..util import ReplyMarkupType


@lru_cache
def list_lessons() -> list[tuple[int, int, str, bool]]:
    columns = [Lesson.id, Lesson.course_id, Lesson.title]
    return session.query(*columns).distinct().all()


@lru_cache
def list_courses() -> Collection[int]:
    return set(e[1] for e in list_lessons())


@lru_cache
def lessons_by_course(course: str) -> list[Lesson]:
    return [
        Lesson(id, course_, title)
        for id, course_, title, sub in list_lessons()
        if course_ == course
    ]


@lru_cache
def get_lesson(id: int) -> Lesson:
    return session.query(Lesson).get(id)


class CourseLessonState():
    name = "CourseLesson"
    item_name = "Урок"

    selected_lesson: Lesson | None = None

#     def get_items(self) -> list[Lesson]:
#         return lessons_by_course(self.)
#
#     def get_lesson(self) -> Lesson:
#         return get_lesson(self.items[self.item_number].id)
#
#     def print_item(self) -> str:
#         lesson = self.get_lesson()
#         text = " ".join(lesson.content.split()[:50])
#         res = [
#             f'<a href="{lesson.image_url}">  </a>',
#             lesson.title,
#             lesson.description,
#             text,
#         ]
#         return "\n\n".join(res)
#
#     def get_buttons(self) -> ReplyMarkupType:
#         # if self.selected_lesson:
#         #     return LessonState.likes_keyboard(self.selected_lesson)
#         return super().get_buttons()
#
class LessonState():
    name = "Lessons"
    substate = CourseLessonState

    def list_courses(self) -> Collection[int]:
        return list_courses()

    def get_item(self, id: int) -> Lesson:
        return get_lesson(id)

