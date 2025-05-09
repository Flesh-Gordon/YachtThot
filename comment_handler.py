from snark_logic import maybe_add_snark
from youtube_client import fetch_song_link
from request_tracker import is_repeat_request, log_request
from genre_detector import detect_genre
from dedication_tracker import extract_dedication

TRIGGER_PREFIX = "yachtthot"

def handle_comment(comment):
    body = comment.body.lower()

    if not body.startswith(TRIGGER_PREFIX):
        return

    query = comment.body[len(TRIGGER_PREFIX):].strip()

    song, link = fetch_song_link(query)
    if not link:
        snark = maybe_add_snark(comment.author.name, genre=None, is_dedication=False, song_found=False)
        comment.reply(f"Couldn't find that track. {snark}")
        return

    genre = detect_genre(song)
    is_repeat = is_repeat_request(comment.author.name, song)
    log_request(comment.author.name, song)

    dedication_target = extract_dedication(query)

    snark = maybe_add_snark(comment.author.name, genre, bool(dedication_target), song_found=True, is_repeat=is_repeat)

    now_playing = f"**NOW PLAYING:** [{song}]({link})"
    if dedication_target:
        now_playing += f" — Dedicated to u/{dedication_target}"

    comment.reply(f"{now_playing}\n\n{snark}")