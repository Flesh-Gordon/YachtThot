from youtube_client import get_video_details
from genre_detector import detect_genre
from snark_logic import maybe_add_snark
from dedication_tracker import extract_dedication

def handle_comment(comment):
    text = comment.body
    author = str(comment.author)

    if not text.lower().startswith("yachtthot"):
        return

    query = text[len("yachtthot"):].strip()
    if not query:
        return

    # Dedication check
    is_dedication, target_user = extract_dedication(query)

    # Search YouTube
    video = get_video_details(query)
    song_found = video is not None
    genre = detect_genre(video["title"]) if song_found else "unknown"

    # Construct response
    if song_found:
        reply = f"**NOW PLAYING:**\n\n[{video['title']}]({video['link']})\n\n"
    else:
        reply = "**NOW PLAYING:**\n\n_No results found._\n\n"

    # Add snark
    snark = maybe_add_snark(author, genre, is_dedication, song_found)
    if snark:
        reply += snark

    comment.reply(reply)