#!/usr/bin/env python3

import json
import re

res: dict[str, list[str]] = {}
arr: list[str]
with open("Факты Psychological Essence.txt", encoding="utf-8-sig") as file:
    for line in file:
        line = line.strip()
        if re.match(r"^[а-яё]+$", line, re.IGNORECASE):
            res[line] = arr = []
        elif m := re.match(r"^[0-9]+\. ", line):
            if arr:
                arr[-1] = re.sub(r"\n+", "\n\n", arr[-1].strip())
            match_len = m.span()[1]
            arr.append(line[match_len:] + "\n")
        else:
            arr[-1] += line + "\n"

json.dump(res, open("data/facts.json", "w"), ensure_ascii=False, indent=2)
