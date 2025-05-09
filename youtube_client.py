from youtubesearchpython import VideosSearch

def get_video_details(query):
    """
    Searches YouTube for the query and returns the video title, channel, and link.
    """
    try:
        videos_search = VideosSearch(query, limit=1)
        result = videos_search.result()
        if result.get("result"):
            video = result["result"][0]
            return {
                "title": video.get("title"),
                "channel": video.get("channel", {}).get("name", "unknown"),
                "link": video.get("link")
            }
        return None
    except Exception as e:
        print(f"[YouTube API ERROR]: {e}")
        return None