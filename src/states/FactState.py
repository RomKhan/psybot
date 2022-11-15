from functools import lru_cache
from random import Random, randint

from ..models import User
from ..util import flatten, load_data_file, oops_message
from .BaseState import BaseState

PAGE_SIZE = 15


def get_headline(fact: str) -> str:
    return fact.split("\n")[0].split(". ")[0]


facts: list[str] = flatten(load_data_file("", "facts").values())
pageable_facts = [(i, get_headline(f)) for i, f in enumerate(facts) if len(get_headline(f)) < 100]


@lru_cache
def get_page(index: int):
    seq = pageable_facts[:]
    rng = Random()
    rng.seed(index)
    rng.shuffle(seq)
    return sorted(seq[:PAGE_SIZE])


class FactState(BaseState):
    name = "Facts"
    fact_number: int
    page_number: int

    def __init__(self, user: User, text: str) -> None:
        super().__init__(user, text)

        self.fact_number = randint(0, len(facts) - 1)
        self.page_number = 0  # todo

    def print_fact(self) -> str:
        return f"Факт №{self.fact_number}\n\n{facts[self.fact_number]}"

    def print_page(self) -> str:
        res = []
        for i, fact in get_page(self.page_number):
            res.append(f"{i}. {fact}")
        return "\n".join(res)

    def next_state(self) -> str | None:
        if self.text.isdigit():
            return "Facts"

        return super().next_state()

    def get_message(self) -> str:
        if self.text.isdigit():
            self.fact_number = int(self.text)
            return self.print_fact()

        match self.text:
            case "Предыдущая страница" | "Следующая страница" | "Факты":
                return f"{self.message}\n\n{self.print_page()}"
            case "Случайный факт":
                return self.print_fact()
            case _:
                return oops_message
