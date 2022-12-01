import typing
from abc import ABC, abstractmethod
from math import ceil
from random import Random, randint

from ..models import User
from ..util import oops_message
from .BaseState import BaseState

PAGE_SIZE = 7


class PageableState(ABC, BaseState):
    random_button: str
    start_button: str

    item_number: int
    page_number: int
    items: typing.Sequence[object]

    is_random: bool = True

    @abstractmethod
    def get_items(self) -> list:
        pass

    @abstractmethod
    def get_headline(self, item: typing.Any) -> str:
        pass

    @abstractmethod
    def print_item(self) -> str:
        pass

    def __init__(self, user: User, text: str) -> None:
        super().__init__(user, text)
        self.reload_items()

        self.page_number = user.page_number or 0

        match self.text:
            case "Предыдущая страница":
                user.page_number = self.page_number - 1
            case "Следующая страница":
                user.page_number = self.page_number + 1

    def reload_items(self) -> None:
        self.items = self.get_items()
        if len(self.items) == 0:
            return

        self.pageable_items = [
            (i, self.get_headline(f))
            for i, f in enumerate(self.items)
            if len(self.get_headline(f)) < 100
        ]

        self.item_number = randint(0, len(self.items) - 1)
        self.message = self.compute_message()

    def get_page(self, index: int):
        if self.is_random:
            seq = self.pageable_items[:]
            rng = Random()
            rng.seed(index)
            rng.shuffle(seq)
            return sorted(seq[:PAGE_SIZE])
        else:
            count = len(self.pageable_items)
            index = index % ceil(count / PAGE_SIZE)
            end = min((index + 1) * PAGE_SIZE, count)
            start = index * PAGE_SIZE
            return self.pageable_items[start:end]

    def print_page(self) -> str:
        res = []
        for i, headline in self.get_page(self.page_number):
            res.append(f"{i+1}. {headline}")
        return "\n".join(res)

    def next_state(self) -> str | None:
        if self.text.isdigit():
            return self.name

        return super().next_state()

    def compute_message(self) -> str:
        if self.text.isdigit():
            self.item_number = int(self.text) - 1
            if self.item_number < 0 or self.item_number >= len(self.items):
                return oops_message
            return self.print_item()

        match self.text:
            case "Предыдущая страница" | "Следующая страница" | self.start_button:
                msg = self.message.replace("{{COUNT}}", str(len(self.items)))
                return f"{msg}\n\n{self.print_page()}"
            case self.random_button:
                return self.print_item()
            case _:
                return oops_message
