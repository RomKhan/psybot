#!/usr/bin/env python3

# todo:
# gapi dl https://docs.google.com/document/d/1qdb3pkK0xR7KD7zAMJiKCXj63Wf7chkHv-JeFTEMeV8

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
            match_len = m.span()[1]
            arr.append(line[match_len:] + "\n")
        else:
            arr[-1] += line + "\n"

for k in res:
    for i in range(len(res[k])):
        res[k][i] = re.sub(r"\n+", "\n\n", res[k][i].strip())

with open("data/facts.json", "w") as f:
    json.dump(res, f, ensure_ascii=False, indent=2, sort_keys=True)
    f.write("\n")
