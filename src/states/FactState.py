import json
import urllib.request

from .PageableState import PageableState
from ..util import ReplyMarkupType
from aiogram.types import InlineKeyboardMarkup

URL = "https://psessence.ru/extapi/facts"


class Fact:
    id: int
    title: str
    content: str

    def __init__(self, id, title, content):
        self.id = id
        self.title = title
        self.content = content

    def __lt__(self, other):
        return self.title < other.title


class FactState(PageableState):
    name = "Facts"
    reco_name = "Fact"
    reco_placeholder = 'прочтения статьи'
    random_button = "🎲 Случайный факт"
    start_button = "💯 Факты"
    selected_fact: Fact | None = None

    def get_items(self) -> list[Fact]:
        items = list[Fact]()
        with urllib.request.urlopen(URL) as response:
            body_json = response.read()
        body_dict = json.loads(body_json)
        for f in body_dict:
            fact = Fact(id=f["id"], title=f["title"], content=f["content"])
            items.append(fact)
        return items

    def get_buttons(self) -> ReplyMarkupType:
        if self.selected_fact:
            kb = InlineKeyboardMarkup(inline_keyboard=[[self.get_recomendation_button(self.name, self.selected_fact.id)]])
            return kb

        return super().get_buttons()

    def get_headline(self, fact: Fact) -> str:
        return fact.title

    def print_page(self) -> str:
        res = []
        for i, headline in self.get_page(self.page_number):
            res.append(f"{i+1}. {headline}")
        return "\n".join(res)

    def print_item(self) -> str:
        self.selected_fact = self.items[self.item_number]
        return f"Факт №{self.item_number+1}\n\n{self.items[self.item_number].title}" \
               f"\n\n{self.items[self.item_number].content.replace('<', '').replace('>', '')}"
