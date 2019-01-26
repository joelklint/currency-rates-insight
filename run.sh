#!/bin/zsh
cd $(dirname "$0")
source .env
cd src
python main.py

