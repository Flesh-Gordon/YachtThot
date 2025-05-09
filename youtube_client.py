import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def get_video_details(video_id):
    request = youtube.videos().list(
        part="snippet,contentDetails",
        id=video_id
    )
    response = request.execute()

    if not response["items"]:
        return None

    item = response["items"][0]
    title = item["snippet"]["title"]
    description = item["snippet"]["description"]
    tags = item["snippet"].get("tags", [])

    return {
        "title": title,
        "description": description,
        "tags": tags
    }
