#!/usr/bin/env python3

import json
import os

obj = json.load(
    open("/home/cortan122/dz2022/командный/zeta-turbine-297107-default-rtdb-export.json")
)

for k in obj["Tests"]:
    try:
        os.mkdir(f"data/quizzes/{k}/")
    except FileExistsError:
        pass

    for k2 in obj["Tests"][k]:
        o = obj["Tests"][k][k2]
        del o["countQuestions"]
        o = {k.lower(): v for k, v in o.items()}
        if "questions" in o:
            o["questions"] = [e.strip() for e in o["questions"]]
        json.dump(o, open(f"data/quizzes/{k}/{k2}.json", "w"), ensure_ascii=False, indent=2)
