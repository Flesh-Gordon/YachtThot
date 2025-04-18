import os
import re
import random
import time
from dotenv import load_dotenv
import openai
import praw
from google.cloud import firestore
from googleapiclient.discovery import build

load_dotenv()

# OpenAI client
from openai import OpenAI
client = OpenAI()

# Firestore
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "firestore_key.json"
db = firestore.Client()

# Reddit API
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD")
)

subreddit = reddit.subreddit("MorganBrennanFanClub")

# YouTube API
youtube = build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"))

def search_youtube(query):
    request = youtube.search().list(q=query, part="snippet", maxResults=1, type="video")
    response = request.execute()
    if response["items"]:
        video = response["items"][0]
        title = video["snippet"]["title"]
        video_id = video["id"]["videoId"]
        return title, f"https://www.youtube.com/watch?v={video_id}"
    return None, None

def should_add_snark(user, song, genre=None, dedicated_to=None):
    if user.lower() == "sdevil713":
        return False

    roll = random.random()
    snark_reasons = []

    if roll < 0.25:
        snark_reasons.append("random")

    # Repeat song logic
    doc_ref = db.collection("requests").document(user)
    doc = doc_ref.get()
    if doc.exists:
        history = doc.to_dict().get("songs", [])
        if history.count(song) >= 1 and random.random() < 0.25:
            snark_reasons.append("repeat")

    # Genre logic
    if genre and random.random() < 0.25:
        snark_reasons.append("genre")

    # Dedication logic
    if genre and dedicated_to and random.random() < 0.25:
        snark_reasons.append("dedication")

    return snark_reasons

def generate_snark(song, user, genre, reasons):
    prompt = f"You are YachtThot, a dramatic party girl bot. A user named {user} requested the song '{song}'"
    if genre:
        prompt += f", which is a {genre} song"
    if reasons:
        prompt += f". The snark is because: {', '.join(reasons)}"
    prompt += ". Respond with a snarky 1-2 sentence comment. Be dramatic, spicy, and flirty."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=80
    )
    return response.choices[0].message.content.strip()

def parse_request(comment):
    match = re.search(r"(?i)yachtthot[:,\-]?\s*(play\s+)?(.+?)(?:\s+for\s+u/(\w+))?$", comment)
    if match:
        song = match.group(2).strip()
        dedication = match.group(3)
        return song, dedication
    return None, None

def main():
    for comment in subreddit.stream.comments(skip_existing=True):
        if comment.author.name == reddit.user.me().name:
            continue

        song, dedication = parse_request(comment.body)
        if not song:
            continue

        user = comment.author.name
        title, url = search_youtube(song)

        doc_ref = db.collection("requests").document(user)
        doc_data = doc_ref.get().to_dict() if doc_ref.get().exists else {}
        song_history = doc_data.get("songs", [])
        song_history.append(song)
        doc_ref.set({"songs": song_history}, merge=True)

        genre = None  # Placeholder for genre detection
        reasons = should_add_snark(user, song, genre, dedicated_to=dedication)
        snark = generate_snark(song, user, genre, reasons) if reasons else ""

        if url:
            reply = f"**NOW PLAYING:**\n\n{title}\n\n▶⠀❙❙⠀■⠀ ─⬤────────── ⠀ 0:01 / 5:27 ⠀ 🔊\n\n{snark}"
        else:
            reply = "Couldn't find the track you're looking for 😬"
            if random.random() < 0.25:
                reply += " (Maybe it's too cringe even for me.)"

        comment.reply(reply)
        print(f"Replied to u/{user} with: {reply}")
        time.sleep(15)

if __name__ == "__main__":
    main()
