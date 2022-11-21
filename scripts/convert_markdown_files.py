#!/usr/bin/env python3

import json
import os
import re

import frontmatter

REPO_URL = "git@github.com:psychological-essence/psychological_essence_articles.git"
REPO_DIR = "psychological_essence_articles"
CONTENT_DIR = f"../{REPO_DIR}/content/articles/"

if not os.path.exists(f"../{REPO_DIR}/"):
    os.system(f"cd .. && git clone {REPO_URL}")

for file in os.listdir(CONTENT_DIR):
    if file[0] == "_":
        continue

    article = frontmatter.load(f"{CONTENT_DIR}/{file}")
    obj = article.metadata
    obj.pop("omit_header_text", None)
    obj["category"] = obj.pop("description")
    obj["content"] = re.sub(r"^#[^\n]+\n", "", article.content.strip()).strip()

    dir = f"data/articles/{obj['category']}/"
    os.makedirs(dir, exist_ok=True)
    jsonfile = f"{dir}/{file.replace('.md', '')}.json"

    with open(jsonfile, "w") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True, default=str)
        f.write("\n")
