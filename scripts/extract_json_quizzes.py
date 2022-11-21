#!/usr/bin/env python3

import json
import os

FILE_PATH = "/home/cortan122/dz2022/командный/zeta-turbine-297107-default-rtdb-export.json"


def lowercase_keys(o: dict) -> dict:
    return {k.lower().replace('"', ""): v for k, v in o.items()}


with open(FILE_PATH) as f:
    obj = json.load(f)

for k in obj["Tests"]:
    os.makedirs(f"data/quizzes/{k}/", exist_ok=True)

    for k2 in obj["Tests"][k]:
        o = lowercase_keys(obj["Tests"][k][k2])
        del o["countquestions"]
        o["category"] = k
        o["filename"] = k2

        # yes, it is misspelled
        if "quetions" in o:
            o["questions"] = o.pop("quetions")
        if "questions" in o:
            o["questions"] = [e.strip() for e in o["questions"] if e]
        if "answers" in o and isinstance(o["answers"], dict):
            o["answers"] = lowercase_keys(o["answers"])
        if "scales" in o and isinstance(o["scales"], dict):
            o["scales"] = lowercase_keys(o["scales"])

        with open(f"data/quizzes/{k}/{k2}.json", "w") as f:
            json.dump(o, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
