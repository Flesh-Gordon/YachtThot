import os
import praw
from dotenv import load_dotenv

# Explicitly load the .env file from the script's directory
load_dotenv(dotenv_path="/home/thefleshgordon/reddit_bot/.env")

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD"),
)