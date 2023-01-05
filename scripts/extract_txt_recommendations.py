#!/usr/bin/env python3

# todo:
# gapi dl https://docs.google.com/document/d/1SrBeQAJWstAxP7vnsuZCduw8qGC5FC2DnOCoSIR3_-c

import json
import re
from glob import glob
from os.path import basename, splitext
from typing import Any


def get_image(query: str) -> str | None:
    fuzzy_query = re.sub(r"[\W_]", "", query.lower())
    return image_dict.get(fuzzy_query)


def get_images(title: str) -> list[str]:
    res = []
    yearless = re.sub(r"\(?[0-9]{4}\)?", "", title)
    res.append(get_image(yearless))

    authorless = re.sub(r"\. .*$", "", title)
    res.append(get_image(authorless))

    authorless = re.sub(r" - .*$", "", title)
    res.append(get_image(authorless))

    quoted = re.search(r'".*?"', title)
    if quoted:
        res.append(get_image(quoted.group(0)))

    quoted = re.search(r"«.*?»", title)
    if quoted:
        res.append(get_image(quoted.group(0)))

    quoted = re.search(r"“.*?”", title)
    if quoted:
        res.append(get_image(quoted.group(0)))

    return [e for e in set(res) if e]


images = glob("../articles/static/images/*/*")
image_dict = {}
for img in images:
    name = re.sub(r"[\W_]", "", splitext(basename(img))[0].lower())
    link = img.replace("../articles/static", "")
    image_dict[name] = link

res: dict[str, list[list[str]]] = {}
arr: list[list[str]]
with open("Рекомендации Psychological Essence.txt", encoding="utf-8-sig") as file:
    for line in file:
        line = line.strip()
        if re.match(r"^[а-яё]+$", line, re.IGNORECASE):
            res[line] = arr = []
        elif m := re.match(r"^[0-9]+\. (.*)\(([а-яё]+)\)$", line, re.IGNORECASE):
            arr.append([m.group(1), "", m.group(2).capitalize()])
        else:
            arr[-1][1] += line + "\n"

res2: dict[str, list[dict[str, Any]]] = {}
for k in res:
    res2[k] = []
    for i in range(len(res[k])):
        key = re.sub(r"(?<=\([0-9]{4})г.(?=\))", "", res[k][i][0].strip())
        value = re.sub(r"\n+", "\n\n", res[k][i][1].strip())

        obj = {
            "title": key,
            "content": value,
            "author": res[k][i][2],
            "image_urls": get_images(key),
            "needs_subscription": False,
        }
        res2[k].append(obj)


def write(name: str, obj: list[dict[str, str]]):
    with open(f"data/recommendations/{name}.json", "w") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


write("Books", res2["Книги"])
write("Films", res2["Фильмы"])
write("Series", res2["Сериалы"])
