#!/bin/sh
rm -rf env
virtualenv -p python2 env
env/bin/pip install -r requirements.txt
