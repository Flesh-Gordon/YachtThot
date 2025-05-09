from googleapiclient.discovery import build
import os

def get_video_details(query):
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        print("[YouTube API ERROR]: Missing API key.")
        return None

    try:
        youtube = build("youtube", "v3", developerKey=api_key)
        request = youtube.search().list(q=query, part="snippet", maxResults=1, type="video")
        response = request.execute()

        if "items" in response and len(response["items"]) > 0:
            item = response["items"][0]
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            return {
                "link": f"https://www.youtube.com/watch?v={video_id}",
                "title": title
            }

        return None

    except Exception as e:
        print(f"[YouTube API ERROR]: {e}")
        return None