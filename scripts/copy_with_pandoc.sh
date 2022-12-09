#!/bin/sh

folder="$1"
dest="$2"

for i in "$folder"/*.docx; do
  file="$dest/$(basename "$i" .docx).md"
  pandoc "$i" -o "$file"
  cat - "$file" <<EOF | sponge "$file"
---
description: Саморазвитие
title: $(basename "$i" .docx)
date: 2022-11-04
docx_url: https://docs.google.com/document/d/1_so4XE6XVGVrl_iTFB0G9Lx_XJmvaL6O
author: Арина
---

EOF
done
