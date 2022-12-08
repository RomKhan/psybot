#!/bin/bash

[ -d env ] || (
  python -m venv env
  . env/bin/activate
  pip install --upgrade pip wheel
  pip install -r requirements.txt
)

. env/bin/activate
export $(xargs <.env)
python main.py
