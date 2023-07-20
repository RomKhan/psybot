import typing

from abc import ABC, abstractmethod
from math import ceil
from random import Random, randint

from ..models import User
from .BaseState import BaseState
from ..util import messages

PAGE_SIZE = 8


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

    @abstractmethod
    def print_recommendation(self) -> str:
        pass

    def __init__(self, user: User, text: str) -> None:
        super().__init__(user, text)
        self.page_number = user.page_number or 0
        self.reload_items()

    def commit(self) -> None:
        self.update_page_number()
        self.message = self.compute_message()
        return super().commit()

    def update_page_number(self) -> None:
        match self.text:
            case "Предыдущая страница":
                self.page_number -= 1
            case "Следующая страница":
                self.page_number += 1
            case self.start_button:
                self.page_number = 0

        self.user.page_number = self.page_number

    def reload_items(self) -> None:
        self.items = sorted(self.get_items())
        if len(self.items) == 0:
            self.pageable_items = []
            return

        self.pageable_items = [
            (i, self.get_headline(f))
            for i, f in enumerate(self.items)
            if len(self.get_headline(f)) < 100
        ]

        self.item_number = randint(0, len(self.items) - 1)

    def get_page(self, index: int):
        if self.is_random:
            seq = self.pageable_items[:]
            rng = Random()
            rng.seed(index)
            rng.shuffle(seq)
            return sorted(seq[:len(self.items)])
        else:
            print(len(self.pageable_items))
            count = len(self.pageable_items)
            index = index % ceil(count / len(self.items))
            end = min((index + 1) * len(self.items), count)
            start = index * len(self.items)
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
                return messages.get("wrong_number")
            return self.print_item()
        match self.text:
            case  "Предыдущая страница" | "Следующая страница" | self.start_button:
                msg = self.message.replace("{{COUNT}}", str(len(self.items)))
                return f"{msg}\n\n{self.print_page()}"
            case self.random_button:
                return self.print_item()
            case _:
                return messages.get("wrong_input")
