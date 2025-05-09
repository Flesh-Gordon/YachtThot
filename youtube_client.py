# youtube_client.py
from youtubesearchpython import VideosSearch

def get_video_details(query):
    try:
        videos_search = VideosSearch(query, limit=1)
        result = videos_search.result()
        if result["result"]:
            video = result["result"][0]
            return {
                "title": video["title"],
                "link": video["link"],
                "duration": video["duration"],
                "channel": video["channel"]["name"],
                "genre": "unknown"  # real genre detection could go here
            }
        return None
    except Exception as e:
        print(f"[YouTube API ERROR]: {e}")
        return None