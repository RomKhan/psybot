from functools import lru_cache
from typing import Collection

from ..database import session
from ..models import Quiz
from ..util import ReplyMarkupType
from .CategoryState import CategoryState
from .LikeableState import LikeableState


@lru_cache
def list_quizzes() -> list[tuple[int, str, str, bool]]:
    columns = [Quiz.id, Quiz.category, Quiz.name, Quiz.needs_subscription]
    return session.query(*columns).distinct().all()


@lru_cache
def list_categories() -> Collection[str]:
    return set(e[1] for e in list_quizzes())


@lru_cache
def quizzes_by_cat(category: str, subscription: bool = False) -> list[tuple[int, str]]:
    return [
        (id, title)
        for id, cat, title, sub in list_quizzes()
        if cat == category and (subscription or not sub)
    ]


@lru_cache
def get_quiz(id: int) -> Quiz:
    return session.query(Quiz).get(id)


class QuizCategoryState(CategoryState):
    name = "QuizCategory"
    random_button = "Случайный тест"
    item_name = "Тест"

    selected_quiz: Quiz | None = None

    def get_items(self) -> list[tuple[int, str]]:
        return quizzes_by_cat(self.category, self.user.is_subscribed())

    def print_item(self) -> str:
        quiz = get_quiz(self.items[self.item_number][0])
        self.selected_quiz = quiz
        res = [
            f"{self.item_name} №{self.item_number+1} в категории «{self.category}»",
            quiz.name,
            quiz.description,
            f"Затрата времени: {quiz.time} минут",
        ]
        return "\n\n".join(res)

    def get_buttons(self) -> ReplyMarkupType:
        # todo: use both keyboards
        # todo: кнопка "начать"
        if self.selected_quiz:
            return QuizzesState.likes_keyboard(self.selected_quiz)
        return super().get_buttons()


class QuizzesState(LikeableState):
    name = "Quizzes"
    substate = QuizCategoryState

    def list_categories(self) -> Collection[str]:
        return list_categories()

    def get_item(self, id: int) -> Quiz:
        return get_quiz(id)
