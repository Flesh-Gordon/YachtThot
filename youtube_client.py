from youtubesearchpython import VideosSearch

def get_video_details(query):
    """
    Searches YouTube for the query and returns details:
    - title
    - link
    - duration
    """
    try:
        videos_search = VideosSearch(query, limit=1)
        result = videos_search.result()
        if result["result"]:
            video = result["result"][0]
            return {
                "title": video.get("title", "Unknown Title"),
                "link": video.get("link"),
                "duration": video.get("duration", "Unknown")
            }
        return None
    except Exception as e:
        print(f"[YouTube API ERROR]: {e}")
        return None