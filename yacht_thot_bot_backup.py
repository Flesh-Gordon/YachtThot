import praw
import re
import random
import time
from googleapiclient.discovery import build

# Reddit API credentials
reddit = praw.Reddit(
    client_id="jflOUZii88YoKMaLlTSORA",  # Updated client ID
    client_secret="UJ6yio9nsWwJarTuLA6nt4sosdlkPQ",
    user_agent="YachtThot/0.2 by /u/TheFleshGordon",
    username="YachtThot",
    password="WhiteSailWitch"
)

# YouTube API key
YOUTUBE_API_KEY = "AIzaSyB90AKBQ7YrHvB8BFiu_bVjNZH03wetWMQ"
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Subreddit to monitor
SUBREDDIT = "supersecretyachtclub"
PROMPT = "YachtThot play"

# List of leader usernames (including the new one)
LEADER_USERNAMES = ["sdevil713", "sdevil7I3", "sdevil7l3"]

# Random responses if no video found
NO_RESULT_RESPONSES = [
    "Couldn't find that, try again dummy",
    "I didn't find anything, BING BONG",
    "Either you can't spell, or you have a learning disability"
]

def search_youtube(query):
    request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q=query,
        type="video"
    )
    response = request.execute()

    if len(response['items']) > 0:
        video = response['items'][0]
        video_id = video['id']['videoId']
        video_title = video['snippet']['title'].replace(" - Topic", "")
        video_channel = video['snippet']['channelTitle']

        video_details_request = youtube.videos().list(
            part="contentDetails",
            id=video_id
        )
        video_details = video_details_request.execute()
        duration = video_details['items'][0]['contentDetails']['duration']

        # Convert YouTube's ISO 8601 duration format to mm:ss
        duration = convert_duration(duration)
        return {
            "title": video_title,
            "channel": video_channel,
            "duration": duration,
            "video_url": f"https://www.youtube.com/watch?v={video_id}"
        }
    else:
        return None

def convert_duration(duration):
    # Convert ISO 8601 duration to mm:ss format
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration)
    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2)) if match.group(2) else 0
    seconds = int(match.group(3)) if match.group(3) else 0

    total_seconds = hours * 3600 + minutes * 60 + seconds
    minutes, seconds = divmod(total_seconds, 60)

    if hours > 0:
        return f"{hours}:{minutes:02}:{seconds:02}"
    else:
        return f"{minutes}:{seconds:02}"

def format_response(video_info, username):
    if username.lower() in [leader.lower() for leader in LEADER_USERNAMES]:
        return f"Here is what you requested Dear Leader:\n\n" \
               f"**NOW PLAYING:**\n\n" \
               f"[{video_info['title']}]({video_info['video_url']})\n\n" \
               f"▶⠀❙❙⠀■⠀ ─⬤────────── ⠀ 0:01 / {video_info['duration']} ⠀ 🔊"
    else:
        return f"**NOW PLAYING:**\n\n" \
               f"[{video_info['title']}]({video_info['video_url']})\n\n" \
               f"▶⠀❙❙⠀■⠀ ─⬤────────── ⠀ 0:01 / {video_info['duration']} ⠀ 🔊"

def handle_no_result(username):
    if username.lower() in [leader.lower() for leader in LEADER_USERNAMES]:
        return "Greatest apologies Dear Leader, I couldn't find your request."
    else:
        return random.choice(NO_RESULT_RESPONSES)

def main():
    try:
        subreddit = reddit.subreddit(SUBREDDIT)
        for comment in subreddit.stream.comments(skip_existing=True):
            if re.search(r'\b' + re.escape(PROMPT) + r'\b', comment.body, re.IGNORECASE):
                parts = comment.body.split(PROMPT, 1)
                if len(parts) > 1:
                    search_query = parts[1].strip()
                    if search_query:
                        video_info = search_youtube(search_query)
                        if video_info:
                            response = format_response(video_info, comment.author.name)
                        else:
                            response = handle_no_result(comment.author.name)
                        comment.reply(response)
                    else:
                        response = handle_no_result(comment.author.name)
                        comment.reply(response)
                else:
                    response = handle_no_result(comment.author.name)
                    comment.reply(response)
    except Exception as e:
        print(f"The bot has stopped running: {e}")
        time.sleep(10)  # Delay before restarting
        main()

if __name__ == "__main__":
    main()
