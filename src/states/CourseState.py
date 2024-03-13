from abc import ABC
from functools import lru_cache
from quizlib.database import session

from ..models import Course, Lesson, User
from ..util import messages, ReplyMarkupType
from .PageableState import PageableState
from aiogram.types import InlineKeyboardMarkup
from .RecommendationManager import RecommendationManager
from aiogram.types import KeyboardButton, InlineKeyboardButton
from .QuizState import QuizState


@lru_cache
def lessons_by_course(course: int) -> list[tuple[int, str]]:
    columns = [Lesson.id, Lesson.name]
    return session.query(*columns).where(Lesson.course_id == course).distinct().all()


@lru_cache
def get_lessons() -> list[tuple[int, str]]:
    columns = [Lesson.id, Lesson.name]
    return session.query(*columns).distinct().all()


@lru_cache
def get_lesson(id: int) -> Lesson:
    return session.query(Lesson).get(id)


@lru_cache
def get_course_by_name(name: str) -> Course:
    return session.query(Course).filter(Course.name == name).first()


class CourseState(PageableState, ABC):
    name = "Course"
    item_name = "Урок"
    course: Course
    course_name: str
    is_random = False
    selected_lesson: Lesson | None = None
    items: list[tuple[int, str]]
    is_subscribed: bool
    need_quiz_message = True

    def get_lesson(self) -> Lesson:
        return get_lesson(self.items[self.item_number][0])

    def get_items(self) -> list[tuple[int, str]]:
        self.course = get_course_by_name(self.course_name)
        if self.course is not None:
            return lessons_by_course(course=self.course.id)
        else:
            return []

    def get_buttons(self) -> ReplyMarkupType:
        return super().get_buttons()

    def mark_as_read(self, lesson: Lesson) -> None:
        lesson.view(self.user.id)
        self.selected_lesson = lesson

    def print_item(self) -> str:
        lesson = self.get_lesson()
        self.mark_as_read(lesson)
        if lesson.description is None:
            lesson.description = ''

        res = [
            lesson.name,
            lesson.description,
            lesson.content,
        ]
        return "\n\n".join(res)

    def print_recommendation(self) -> str:
        return ''

    def get_buttons(self) -> ReplyMarkupType:
        if self.selected_lesson and self.selected_lesson.quiz_id is not None:
            btn = InlineKeyboardButton('Пройти тест', callback_data=f"{QuizState.name}/{self.selected_lesson.quiz_id}/0/start:0")
            kb = InlineKeyboardMarkup([[btn]])
            kb.row(btn)
            return kb

        return super().get_buttons()

    def get_message(self) -> str:
        lessons_cnt = len(lessons_by_course(course=self.course.id))
        if self.course.needs_subscription and not self.is_subscribed:
            return self.data["message403"]

        if self.text == self.course_name or self.text == "Предыдущая страница" or self.text == "Текущая страница" or self.text == "Следующая страница":
                res = [self.course.description,
                       "# Длительность: " + self.course.duration,

                       self.message.replace("{{COUNT}}", str(lessons_cnt))
                       ]
                self.recommendation_message = self.print_recommendation()
                self.need_recommendation = True
                return "\n\n".join(res)
        elif self.text.isdigit() and lessons_cnt >= int(self.text) > 0:
            return self.print_item()
        else:
            return messages["wrong_input"]

    def __init__(self, user: User, text: str):
        self.course_name = ""
        self.is_subscribed = user.is_subscribed()
        super().__init__(user, text)

    def get_headline(self, item: Lesson) -> str:
        return item.name

    def set_substate(self, *args: str) -> None:
        assert len(args) == 1
        self.start_button = self.course_name = args[0]
        self.course_name = args[0]
        self.course = get_course_by_name(self.course_name)
        self.start_button = self.start_button[:32]
        # todo: translate name
        self.name = f"{self.name}/{self.course_name}"
        self.reload_items()
