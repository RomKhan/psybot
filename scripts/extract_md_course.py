#!/usr/bin/env python3

import json
import os.path
import re
import sys
import unicodedata


def advance_data(m: re.Match) -> None:
    global data
    i = m.end()
    data = data[i:]


dir = os.path.dirname(sys.argv[1])
course_name = "Манипуляции"
lessons: list[dict] = []

with open(f"{dir}/Курс_{course_name}.md") as file:
    data = unicodedata.normalize("NFC", file.read())
    while True:
        m = re.search(r"^Урок ([0-9]+)\. (.+)\\?$", data, re.MULTILINE)
        if not m:
            m = re.search(r"^()(Манипуляции в .+)\\?$", data, re.MULTILINE)
            if not m:
                break
        advance_data(m)

        name = m.group(2).strip()
        description = None
        content = None
        m = re.match(r"^\n*\*\*Описание(?: урока)?:\*\* ([\S\s]*?)\n\n", data)
        if m:
            description = re.sub(r"[ \n]+", " ", m.group(1).strip())
            advance_data(m)

        m = re.search("^Тест$", data, re.MULTILINE)
        assert m
        content_end = m.start()
        content = re.sub(r"^ +> ", "", data[:content_end].strip(), flags=re.MULTILINE)
        advance_data(m)

        quiz_name = f"Курс{course_name}_Урок{len(lessons)+1}"
        lessons.append(
            {"name": name, "content": content, "description": description, "quiz_name": quiz_name}
        )

res = {
    "lessons": lessons,
    "name": course_name,
    "description": "# О курсе\nПока ничего не известно. Курс -- энигма. Так и живём...",
    "needs_subscription": False,
    "duration": "2 месяца",
}

with open(f"data/courses/{course_name}.json", "w") as f:
    json.dump(res, f, ensure_ascii=False, indent=2, sort_keys=True)
    f.write("\n")
