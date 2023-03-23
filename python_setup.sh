#!/bin/bash

[ ! -d env ] && python -m venv env
source pyenv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
