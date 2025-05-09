from youtubesearchpython import VideosSearch

def get_youtube_link(query):
    """
    Searches YouTube for the query and returns the first video URL found.
    """
    try:
        videos_search = VideosSearch(query, limit=1)
        result = videos_search.result()
        if result["result"]:
            return result["result"][0]["link"]
        return None
    except Exception as e:
        print(f"[YouTube API ERROR]: {e}")
        return None