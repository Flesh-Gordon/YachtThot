GENRE_KEYWORDS = {
    "hip hop": "hip-hop",
    "rap": "hip-hop",
    "country": "bro-country",
    "pop": "pop",
    "edm": "edm",
    "hyperpop": "hyperpop",
    "trap": "hip-hop",
    "rock": "rock",
    "indie": "indie",
    "reggaeton": "latin",
    "jazz": "jazz",
    "kpop": "k-pop"
}

def detect_genre(title, description="", tags=None):
    text = f"{title} {description}".lower()
    tags = tags or []

    for keyword, genre in GENRE_KEYWORDS.items():
        if keyword in text or any(keyword in tag.lower() for tag in tags):
            return genre

    return "unknown"
