#!/usr/bin/env python3

import json

from quizlib.database import engine, session
from quizlib.environment import DATA_DIR, ECHO_SQL
from quizlib.models import Recommendation

engine.echo = ECHO_SQL


def backport_category(cat: str):
    lst = session.query(Recommendation).where(Recommendation.category == cat).all()
    res = []

    for rec in lst:
        dct = rec.to_dict()
        del dct["id"]
        del dct["category"]
        del dct["year"]
        del dct["country"]
        del dct["genre"]
        for k in list(dct):
            if dct[k] is None:
                del dct[k]
        res.append(dct)

    with open(f"{DATA_DIR}/recommendations/{cat}.json", "w") as f:
        json.dump(res, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


backport_category("Books")
backport_category("Films")
backport_category("Series")
