from snark_pool import get_snark_reply
from dotenv import load_dotenv
import os
import praw
import re
import random
import time
import json
import sys
import fcntl
import datetime
from googleapiclient.discovery import build

load_dotenv(dotenv_path=".env")

# Lockfile
lock_file = open('/home/thefleshgordon/yachtbot.lock', 'w')
try:
    fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
except BlockingIOError:
    print("Another instance is already running. Exiting.")
    sys.exit(1)

# Reddit API
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_SECRET"),
    user_agent="YachtThot/0.2 by /u/TheFleshGordon",
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD")
)

# YouTube
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

SUBREDDIT = "MorganBrennanFanClub"
PROMPT = "YachtThot play"
DJ_PROMPT = "YachtThot be my DJ"
DEDICATE_PROMPT = "dedicate"

REPLIED_FILE = "replied_to.json"
if os.path.exists(REPLIED_FILE):
    with open(REPLIED_FILE, "r") as f:
        replied_to = set(json.load(f))
else:
    replied_to = set()

LEADER_USERNAMES = ["sdevil713", "sdevil7I3", "sdevil7l3"]
NO_RESULT_RESPONSES = [
    "Couldn't find that, try again dummy.",
    "I didn't find anything, BING BONG.",
    "Either you can't spell, or you have a learning disability."
]

RANDOM_SEARCH_TERMS = [...]
GAY_GENRE_SEARCH_TERMS = [...]

def search_youtube(query):
    request = youtube.search().list(part="snippet", maxResults=1, q=query, type="video")
    response = request.execute()
    if response['items']:
        video = response['items'][0]
        video_id = video['id']['videoId']
        title = video['snippet']['title'].replace(" - Topic", "")
        duration_data = youtube.videos().list(part="contentDetails", id=video_id).execute()
        duration = convert_duration(duration_data['items'][0]['contentDetails']['duration'])
        return {"title": title, "duration": duration, "video_url": f"https://www.youtube.com/watch?v={video_id}"}
    return None

def convert_duration(duration):
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration)
    h = int(match.group(1) or 0)
    m = int(match.group(2) or 0)
    s = int(match.group(3) or 0)
    m, s = divmod(h * 3600 + m * 60 + s, 60)
    return f"{h}:{m:02}:{s:02}" if h else f"{m}:{s:02}"

def format_response(video, username, dedication=None):
    line = f"[{video['title']}]({video['video_url']})"
    bar = f"▶⠀❙❙⠀■⠀ ─⬤────────── ⠀ 0:01 / {video['duration']} ⠀ 🔊"
    base = f"**NOW PLAYING:**\n\n{line}\n\n{bar}"

    if dedication:
        dedication = dedication if dedication.startswith("u/") else f"u/{dedication}"
        snark = get_snark_reply()
        return f"{base}\n\nDedicated to {dedication} — {snark}"

    if username.lower() in [u.lower() for u in LEADER_USERNAMES]:
        return f"Here is what you requested Dear Leader:\n\n{base}"

    if random.random() < 0.25:
        return base + "\n\n" + get_snark_reply()
    return base

def handle_no_result(username, dedication=None):
    base = (
        "Greatest apologies Dear Leader, I couldn't find your request."
        if username.lower() in [u.lower() for u in LEADER_USERNAMES]
        else random.choice(NO_RESULT_RESPONSES)
    )
    if dedication:
        base += " " + get_snark_reply()
    elif random.random() < 0.25:
        base += " " + get_snark_reply()
    return base

def main():
    try:
        subreddit = reddit.subreddit(SUBREDDIT)
        for comment in subreddit.stream.comments(skip_existing=True):
            if comment.id in replied_to:
                continue

            created_utc = datetime.datetime.utcfromtimestamp(comment.created_utc)
            if (datetime.datetime.utcnow() - created_utc).total_seconds() > 60:
                continue

            body = comment.body.strip()
            username = comment.author.name
            print(f"New comment from u/{username}: {body}")
            response = None

            lower = body.lower()

            if "yachthot play" in lower:
                response = "Learn to Spell"

            elif "yachtthot be my dj" in lower:
                video = search_youtube(random.choice(RANDOM_SEARCH_TERMS))
                response = format_response(video, username) if video else handle_no_result(username)

            elif "yachtthot play" in lower and username.lower() == "flyingmadlad":
                video = search_youtube(random.choice(GAY_GENRE_SEARCH_TERMS))
                response = format_response(video, username) if video else handle_no_result(username)

            elif lower.startswith("dedicate"):
                match = re.match(r'dedicate\s+(.+?)\s+to\s+(.+)', body, re.IGNORECASE)
                if match:
                    song, target = match.groups()
                    video = search_youtube(song.strip())
                    response = format_response(video, username, target.strip()) if video else handle_no_result(username, target.strip())

            elif "yachtthot play" in lower:
                parts = re.split(re.escape(PROMPT), body, maxsplit=1, flags=re.IGNORECASE)
                if len(parts) > 1:
                    query = parts[1].strip()
                    if query:
                        video = search_youtube(query)
                        response = format_response(video, username) if video else handle_no_result(username)
                    else:
                        response = handle_no_result(username)

            if response:
                comment.reply(response)
                replied_to.add(comment.id)
                with open(REPLIED_FILE, "w") as f:
                    json.dump(list(replied_to), f)

    except Exception as e:
        print(f"The bot crashed: {e}")
        time.sleep(10)
        main()

if __name__ == "__main__":
    main()