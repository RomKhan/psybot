from .AppDownloadState import AppDownloadState
from .ArticleState import ArticleCategoryState, ArticleState
from .BaseState import BaseState
from .BookRecommendationState import BookRecommendationState
from .FactState import FactState
from .FilmRecommendationState import FilmRecommendationState
from .LikeableState import LikeableState
from .LoginState import FailedLoginState, LoginState, SuccessfulLoginState
from .PageableState import PageableState
from .QuizState import QuizState
from .QuizzesState import QuizCategoryState, QuizzesState
from .SeriesRecommendationState import SeriesRecommendationState
from .SubscribeState import SubscribeState
from .TechniqueState import TechniqueCategoryState, TechniqueState
from .UnsubscribeState import UnsubscribeState

__all__ = [
    "BaseState",
    "LikeableState",
    "PageableState",
    "FactState",
    "ArticleState",
    "BookRecommendationState",
    "SeriesRecommendationState",
    "FilmRecommendationState",
    "ArticleCategoryState",
    "ArticleState",
    "TechniqueCategoryState",
    "TechniqueState",
    "QuizCategoryState",
    "QuizzesState",
    "QuizState",
    "AppDownloadState",
    "SubscribeState",
    "LoginState",
    "UnsubscribeState",
]


def make_state(name: str) -> type[BaseState]:
    return type(f"{name}State", (BaseState,), {"name": name})


states_by_name: dict[str, type[BaseState]] = {
    "Start": make_state("Start"),
    "NotImplemented": make_state("NotImplemented"),
    "Recommendations": make_state("Recommendations"),
    "FailedLogin": FailedLoginState,
    "SuccessfulLogin": SuccessfulLoginState,
    "Facts": FactState,
    "BookRecommendations": BookRecommendationState,
    "SeriesRecommendations": SeriesRecommendationState,
    "FilmRecommendations": FilmRecommendationState,
    "Articles": ArticleState,
    "ArticleCategory": ArticleCategoryState,
    "Techniques": TechniqueState,
    "TechniqueCategory": TechniqueCategoryState,
    "Quizzes": QuizzesState,
    "QuizCategory": QuizCategoryState,
    "Quiz": QuizState,
    "AppDownload": AppDownloadState,
    "Subscribe": SubscribeState,
    "Login": LoginState,
    "Unsubscribe": UnsubscribeState,
}
