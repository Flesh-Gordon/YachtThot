from snark_pool import get_snark_reply
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")  # Explicit path

print(os.getenv("REDDIT_PASSWORD"))  # Optional debug
import praw
import re
import random
import time
import json
import os
import sys
import fcntl
import datetime
from googleapiclient.discovery import build

# Lockfile to prevent multiple instances
lock_file = open('/home/thefleshgordon/yachtbot.lock', 'w')
try:
    fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
except BlockingIOError:
    print("Another instance is already running. Exiting.")
    sys.exit(1)

# Reddit API credentials
reddit = praw.Reddit(
    client_id="w_ZViACUvzEzxjeyy9DOSw",
    client_secret="n-FXhLT3XskU6lXHFlaTHtD7s5ORZw",
    user_agent="YachtThot/0.2 by /u/TheFleshGordon",
    username="YachtThotv2_Test",
    password="YachtThotTest"
)

# YouTube API setup
YOUTUBE_API_KEY = "AIzaSyB90AKBQ7YrHvB8BFiu_bVjNZH03wetWMQ"
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Subreddit and prompts
SUBREDDIT = "MorganBrennanFanClub"
PROMPT = "YachtThot play"
DJ_PROMPT = "YachtThot be my DJ"

# Track replies
REPLIED_FILE = "replied_to.json"
if os.path.exists(REPLIED_FILE):
    with open(REPLIED_FILE, "r") as f:
        replied_to = set(json.load(f))
else:
    replied_to = set()

# Special users
LEADER_USERNAMES = ["sdevil713", "sdevil7I3", "sdevil7l3"]

# Fallback replies
NO_RESULT_RESPONSES = [
    "Couldn't find that, try again dummy",
    "I didn't find anything, BING BONG",
    "Either you can't spell, or you have a learning disability"
]

# Music genre pools
RANDOM_SEARCH_TERMS = [
    "lofi beats", "chill music", "vaporwave", "jazzhop", "indie pop", "ambient synth",
    "classical piano", "synthwave", "trap instrumental", "funk groove", "deep house",
    "future bass", "reggae vibes", "acoustic covers", "classic rock", "k-pop hits",
    "edm festival mix", "techno workout", "blues guitar", "melodic dubstep", "folk music",
    "latin pop", "instrumental chill", "hip hop 90s", "r&b soul mix", "psytrance journey",
    "epic orchestral", "japanese city pop", "french cafe music", "caribbean dancehall",
    "bedroom pop", "ambient rain sounds"
]

GAY_GENRE_SEARCH_TERMS = [
    "gay anthems", "lgbtq playlist", "pride party mix", "drag queen performance music",
    "troye sivan hits", "rupaul songs", "hyperpop queer playlist", "sam smith best songs",
    "lady gaga essentials", "kim petras mix", "queer indie pop", "club remixes pride"
]

def search_youtube(query):
    request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q=query,
        type="video"
    )
    response = request.execute()

    if response['items']:
        video = response['items'][0]
        video_id = video['id']['videoId']
        title = video['snippet']['title'].replace(" - Topic", "")
        channel = video['snippet']['channelTitle']
        duration_data = youtube.videos().list(part="contentDetails", id=video_id).execute()
        duration = convert_duration(duration_data['items'][0]['contentDetails']['duration'])

        return {
            "title": title,
            "channel": channel,
            "duration": duration,
            "video_url": f"https://www.youtube.com/watch?v={video_id}"
        }
    return None

def convert_duration(duration):
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration)
    h = int(match.group(1)) if match.group(1) else 0
    m = int(match.group(2)) if match.group(2) else 0
    s = int(match.group(3)) if match.group(3) else 0
    total = h * 3600 + m * 60 + s
    m, s = divmod(total, 60)
    return f"{h}:{m:02}:{s:02}" if h else f"{m}:{s:02}"

def format_response(video, username):
    base = f"**NOW PLAYING:**\n\n[{video['title']}]({video['video_url']})\n\n" \
           f"▶⠀❙❙⠀■⠀ ─⬤────────── ⠀ 0:01 / {video['duration']} ⠀ 🔊"
    if username.lower() in [u.lower() for u in LEADER_USERNAMES]:
        return f"Here is what you requested Dear Leader:\n\n{base}"
    if random.random() < 0.25:
        return base + "\n\n" + get_snark_reply()
    return base

def handle_no_result(username):
    if username.lower() in [u.lower() for u in LEADER_USERNAMES]:
        return "Greatest apologies Dear Leader, I couldn't find your request."
    msg = random.choice(NO_RESULT_RESPONSES)
    if random.random() < 0.25:
        msg += " " + get_snark_reply()
    return msg

def main():
    try:
        subreddit = reddit.subreddit(SUBREDDIT)
        for comment in subreddit.stream.comments(skip_existing=True):
            if comment.id in replied_to:
                continue

            # Skip comments older than 60 seconds
            created_utc = datetime.datetime.utcfromtimestamp(comment.created_utc)
            now = datetime.datetime.utcnow()
            age = (now - created_utc).total_seconds()
            if age > 60:
                continue

            body = comment.body.strip()
            body_lower = body.lower()
            username = comment.author.name
            print(f"⏺️  New comment from u/{username}: {body}")

            response = None

            if "yachthot play" in body_lower:
                response = "Learn to Spell"

            elif "yachtthot be my dj" in body_lower:
                query = random.choice(RANDOM_SEARCH_TERMS)
                video = search_youtube(query)
                response = format_response(video, username) if video else handle_no_result(username)

            elif "yachtthot play" in body_lower and username.lower() == "flyingmadlad":
                query = random.choice(GAY_GENRE_SEARCH_TERMS)
                video = search_youtube(query)
                response = format_response(video, username) if video else handle_no_result(username)

            elif "yachtthot play" in body_lower:
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
