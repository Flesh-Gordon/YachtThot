# request_tracker.py

user_requests = {}

def is_repeat_request(username, song_title):
    user = username.lower()
    song = song_title.lower()
    if user in user_requests and song in user_requests[user]:
        return True
    return False

def log_request(username, song_title):
    user = username.lower()
    song = song_title.lower()
    if user not in user_requests:
        user_requests[user] = set()
    user_requests[user].add(song)