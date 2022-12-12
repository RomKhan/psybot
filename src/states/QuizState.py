from functools import lru_cache

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from ..database import session
from ..models import Quiz
from ..util import ReplyMarkupType
from .BaseState import BaseState


@lru_cache
def get_quiz(id: int) -> Quiz:
    # todo: cache questions and answers
    return session.query(Quiz).get(id)


class QuizState(BaseState):
    name = "Quiz"
    quiz: Quiz
    question_index: int
    num_questions: int

    def set_substate(self, *args: str) -> None:
        assert len(args) == 2
        self.quiz = get_quiz(int(args[0]))
        self.question_index = int(args[1])
        self.num_questions = max(len(self.quiz.questions), len(self.quiz.answers))  # type: ignore
        self.name = f"{self.name}/{self.quiz.id}/{self.question_index}"

    def get_message(self) -> str:
        if self.question_index >= self.num_questions:
            return "Вопросов больше нет, идём домой ребятки 0_0"

        res = super().get_message()
        res = res.replace("{{INDEX}}", str(self.question_index + 1))
        res = res.replace("{{NAME}}", str(self.quiz.name))
        res += f"\n\n{self.get_question()}"
        return res

    def get_answers(self) -> list[str]:
        arr: list[list[str]] = self.quiz.answers  # type: ignore
        return arr[self.question_index % len(arr)]

    def get_question(self) -> str:
        arr: list[str] = self.quiz.questions  # type: ignore
        return arr[self.question_index % len(arr)]

    def get_buttons(self) -> ReplyMarkupType:
        res = InlineKeyboardMarkup(row_width=2)
        name = f"{self.__class__.name}/{self.quiz.id}"

        if self.question_index >= self.num_questions:
            action = f"{name}/{self.question_index-1}/end:0"  # todo: different state?
            res.add(InlineKeyboardButton(text=self.buttons[-1][2], callback_data=action))
        else:
            for i, ans in enumerate(self.get_answers()):
                action = f"{name}/{self.question_index+1}/answer:{i}"
                res.insert(InlineKeyboardButton(text=ans, callback_data=action))

        if self.question_index:
            action = f"{name}/{self.question_index-1}/goto:0"
            res.add(InlineKeyboardButton(text=self.buttons[-1][0], callback_data=action))
        else:
            action = f"QuizCategory/{self.quiz.category}/show:{self.quiz.id}"
            res.add(InlineKeyboardButton(text=self.buttons[-1][1], callback_data=action))

        return res

    def action(self, action: str, pram: int) -> None:
        if action == "goto" or action == "start":
            pass
        elif action == "answer":
            self.message += f"\nanswer {pram}"  # todo
        else:
            return super().action(action, pram)
