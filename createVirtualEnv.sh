#!/bin/sh
rm -rf env
python3 -m venv env
env/bin/pip install -U pip
env/bin/pip install -r requirements.txt
