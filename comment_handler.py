from youtube_client import get_video_details
from genre_detector import detect_genre
from snark_logic import maybe_add_snark
from youtube_search import get_youtube_link
import re

def extract_video_id(youtube_url):
    match = re.search(r"(?:v=|youtu.be/)([\w-]{11})", youtube_url)
    return match.group(1) if match else None

def handle_comment(comment):
    text = comment.body
    username = comment.author.name

    match = re.search(r"YachtThot\s+play\s+(.+)", text, re.IGNORECASE)
    if not match:
        return

    song_request = match.group(1).strip()
    video_url = get_youtube_link(song_request)
    video_id = extract_video_id(video_url)

    genre = "unknown"
    if video_id:
        video_data = get_video_details(video_id)
        if video_data:
            genre = detect_genre(
                title=video_data["title"],
                description=video_data["description"],
                tags=video_data["tags"]
            )

    snark = maybe_add_snark(username=username, genre=genre, is_dedication=False, is_repeat=False, song_found=True)

    reply_text = f"**NOW PLAYING:**\n\n[{video_data['title']}]({video_url})\n\n{snark}" if video_data else "Could not find a matching song."
    comment.reply(reply_text)