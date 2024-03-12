#!/usr/bin/env python3

import random

from quizlib.api import qizz_results

arr = [
    "Полностью не согласен",
    "Не согласен",
    "Скорее не согласен",
    "Затрудняюсь ответить",
    "Скорее согласен",
    "Согласен",
    "Полностью согласен",
]


def lst(arr: list[str], n: int) -> list[str]:
    return [random.choice(arr) for _ in range(n)]


print(qizz_results("Характер, личностные качества/ImplicitTheoriesLearning", lst(arr, 24)))

print("=" * 80)

arr = [
    "Абсолютно не согласен",
    "Не согласен",
    "Скорее не согласен",
    "Затрудняюсь ответить",
    "Скорее согласен",
    "Согласен",
    "Абсолютно согласен",
]

print(qizz_results("CharacterOfUser/CognitiveFlexibilityQuestionnaire", lst(arr, 20)))

print("=" * 80)

arr = ["Нет", "Скорее нет", "Скорее да", "Да"]

print(qizz_results("CharacterOfUser/HardinessSurvey", lst(arr, 45)))

print("=" * 80)

arr = [
    "Совершенно не согласен",
    "Не согласен, но бывают исключения",
    "Чаще не согласен",
    "50/50",
    "Чаще согласен",
    "Согласен, но бывают исключения",
    "Совершенно согласен",
]

print(qizz_results("CharacterOfUser/MultidimensionalPerfectionismScale", lst(arr, 45)))
