import re
from youtube_client import get_video_details
from genre_detector import detect_genre
from snark_logic import maybe_add_snark
from dedication_tracker import extract_dedication

def handle_comment(comment):
    text = comment.body
    author = str(comment.author)

    # Check for play command
    match = re.search(r"YachtThot\s+play\s+(.+)", text, re.IGNORECASE)
    if not match:
        return

    query = match.group(1).strip()
    is_dedication, target_user = extract_dedication(query)
    video = get_video_details(query)

    if video:
        genre = detect_genre(video["title"], video["channel"])
        snark = maybe_add_snark(author, genre, is_dedication=is_dedication, is_repeat=False)
        response = (
            f"**NOW PLAYING:**\n\n"
            f"[{video['title']}]({video['link']})\n\n"
        )
    else:
        genre = "unknown"
        snark = maybe_add_snark(author, genre, is_dedication=is_dedication, song_found=False)
        response = "**NOW PLAYING:**\n\n*No results found.*\n\n"

    if snark:
        response += f"{snark}\n"

    comment.reply(response.strip())