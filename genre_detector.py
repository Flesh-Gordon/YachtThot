import re

GENRE_KEYWORDS = {
    "bro-country": ["florida georgia line", "luke bryan"],
    "hyperpop": ["100 gecs", "charli xcx", "dorian electra"],
    "eurodance": ["aqua", "vengaboys", "eiffel 65"],
    "hip hop": ["ying yang twins", "missy elliott", "lil jon"],
}

def detect_genre(title, channel):
    query = f"{title} {channel}".lower()
    for genre, keywords in GENRE_KEYWORDS.items():
        for keyword in keywords:
            if re.search(rf"\b{re.escape(keyword)}\b", query):
                return genre
    return "unknown"