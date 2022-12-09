#!/usr/bin/env python3

import json
import os
import re

import frontmatter

REPO_URL = "git@github.com:psychological-essence/psychological_essence_articles.git"
REPO_DIR = "articles"
CONTENT_DIR = f"../{REPO_DIR}/content/"

if not os.path.exists(f"../{REPO_DIR}/"):
    os.system(f"cd .. && git clone {REPO_URL} {REPO_DIR}")


def transfer_dir(category: str):
    content_dir = f"{CONTENT_DIR}/{category}"

    for file in os.listdir(content_dir):
        if file[0] == "_":
            continue

        article = frontmatter.load(f"{content_dir}/{file}")
        obj = article.metadata
        obj.pop("omit_header_text", None)
        obj["category"] = obj.pop("description")
        obj["content"] = re.sub(r"^#[^\n]+\n", "", article.content.strip()).strip()
        url_name = re.sub(r"[^а-яёa-z]+", "-", file.replace(".md", "").lower())
        obj["url"] = f"/{category}/{url_name}/"

        dirname = f"data/{category}/{obj['category']}/"
        os.makedirs(dirname, exist_ok=True)
        jsonfile = f"{dirname}/{file.replace('.md', '.json')}"

        with open(jsonfile, "w") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True, default=str)
            f.write("\n")


transfer_dir("articles")
transfer_dir("techniques")
