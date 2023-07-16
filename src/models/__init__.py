from quizlib.models import (
    ActionLog,
    AndroidUser,
    Article,
    Order,
    Quiz,
    QuizResult,
    Recommendation,
    Technique,
    Course,
    Lesson,
    ModelRecommendation,
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
    "Order",
    "Lesson",
    "Course",
    "ModelRecommendation",
]

Base.metadata.create_all(engine)
