from youtubesearchpython import VideosSearch

def get_video_details(query):
    try:
        search = VideosSearch(query, limit=1)
        results = search.result()
        if results.get("result"):
            video = results["result"][0]
            return {
                "title": video.get("title"),
                "channel": video.get("channel", {}).get("name", "unknown"),
                "link": video.get("link")
            }
        return None
    except Exception as e:
        print(f"[YouTube API ERROR]: {e}")
        return None