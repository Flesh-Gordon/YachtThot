#!/bin/bash

cd /home/thefleshgordon/reddit_bot || exit

# Optional: load .env manually if needed
# export $(grep -v '^#' .env | xargs)

source venv/bin/activate
python3 main.py