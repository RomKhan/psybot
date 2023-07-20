import json
import markdown
import urllib.request

from .RecommendationManager import RecommendationManager
from ..util import flatten, load_data_file
from .PageableState import PageableState

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
    def print_recommendation(self) -> str:
        try:
            manager = RecommendationManager(self.items[self.item_number].id, "Fact")
            return manager.get_message().replace("{{STATE}}", "прочтения статьи")
        except (Exception,):
            return ""

    name = "Facts"
    random_button = "Случайный факт"
    start_button = "Факты"

    def get_items(self) -> list[Fact]:
        items = list[Fact]()
        with urllib.request.urlopen(URL) as response:
            body_json = response.read()
        body_dict = json.loads(body_json)
        for f in body_dict:
            fact = Fact(id=f["id"], title=f["title"], content=f["content"])
            items.append(fact)
        # return flatten(load_data_file("", "facts").values())
        return items

    def get_headline(self, fact: Fact) -> str:
        # return fact.split("\n")[0].split(". ")[0]
        return fact.title

    def print_page(self) -> str:
        res = []
        for i, headline in self.get_page(self.page_number):
            if (i + 1) % 5 == 0:
                res.append(f"{i+1}. {headline}")
        return "\n".join(res)

    def print_item(self) -> str:
        self.recommendation_message = self.print_recommendation()
        self.need_recommendation = True
        return f"Факт №{self.item_number+1}\n\n{self.items[self.item_number].title}" \
               f"\n\n{self.items[self.item_number].content.replace('<', '').replace('>', '')}"
