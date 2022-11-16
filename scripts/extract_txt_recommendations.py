#!/usr/bin/env python3

# todo:
# gapi dl https://docs.google.com/document/d/1SrBeQAJWstAxP7vnsuZCduw8qGC5FC2DnOCoSIR3_-c

import json
import re

res: dict[str, list[list[str]]] = {}
arr: list[list[str]]
with open("Рекомендации Psychological Essence.txt", encoding="utf-8-sig") as file:
    for line in file:
        line = line.strip()
        if re.match(r"^[а-яё]+$", line, re.IGNORECASE):
            res[line] = arr = []
        elif m := re.match(r"^[0-9]+\. (.*)\([а-яё]+\)$", line, re.IGNORECASE):
            arr.append([m.group(1), ""])
        else:
            arr[-1][1] += line + "\n"

res2: dict[str, dict[str, str]] = {}
for k in res:
    res2[k] = {}
    for i in range(len(res[k])):
        key = re.sub(r"(?<=\([0-9]{4})г.(?=\))", "", res[k][i][0].strip())
        value = re.sub(r"\n+", "\n\n", res[k][i][1].strip())
        res2[k][key] = value


def write(name: str, obj: dict[str, str]):
    with open(f"data/recommendations/{name}.json", "w") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


write("Books", res2["Книги"])
write("Films", res2["Фильмы"])
write("Series", res2["Сериалы"])
