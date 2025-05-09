# genre_detector.py

def detect_genre(song_title):
    lowered = song_title.lower()

    if any(term in lowered for term in ["luke bryan", "florida georgia line", "jason aldean"]):
        return "bro-country"
    elif any(term in lowered for term in ["hyperpop", "100 gecs", "bladee"]):
        return "hyperpop"
    elif "edm" in lowered or "rave" in lowered:
        return "edm"
    else:
        return "unknown"