# comment_handler.py

from youtube_client import get_video_details
from genre_detector import detect_genre
from dedication_tracker import extract_dedication
from snark_logic import maybe_add_snark

def handle_comment(comment):
    query = comment.body.lower().replace("yachtthot", "").strip()

    # Dedication detection
    dedication_result = extract_dedication(query)
    is_dedication = False
    target_user = None
    if dedication_result:
        is_dedication = True
        target_user = dedication_result

    # YouTube search
    video = get_video_details(query)

    # No result case
    if not video:
        snark = maybe_add_snark(comment.author.name, genre=None, is_dedication=is_dedication, song_found=False)
        response = "**NOW PLAYING:**  \n*No results found.*"
        if snark:
            response += f"\n\n{snark}"
        comment.reply(response)
        return

    # Genre detection
    genre = detect_genre(video['title'], video['channel'])

    # Snark logic
    is_repeat = False  # You can implement repeat logic here if needed
    snark = maybe_add_snark(comment.author.name, genre, is_dedication=is_dedication, is_repeat=is_repeat)

    # Final formatted reply
    response = f"""**NOW PLAYING:**  
[{video['title']}]({video['url']})  
  
{snark}""" if snark else f"""**NOW PLAYING:**  
[{video['title']}]({video['url']})"""

    comment.reply(response)