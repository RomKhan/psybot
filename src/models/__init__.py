from quizlib.models import (
    ActionLog,
    AndroidUser,
    Article,
    Quiz,
    QuizResult,
    Recommendation,
    Technique,
)
from quizlib.models import TelegramUser as User

from ..database import Base, engine
from .QuizAnswer import QuizAnswer

__all__ = [
    "ActionLog",
    "User",
    "Article",
    "Quiz",
    "Technique",
    "QuizAnswer",
    "QuizResult",
    "Recommendation",
    "AndroidUser",
]

Base.metadata.create_all(engine)
