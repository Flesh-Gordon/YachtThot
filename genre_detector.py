import re

GENRE_KEYWORDS = {
    "bro-country": ["florida georgia line", "luke bryan", "jason aldean"],
    "hyperpop": ["100 gecs", "hyperpop", "glaive", "osquinn"],
    "eurodance": ["aqua", "eiffel 65", "eurodance", "2 unlimited"],
    "classic rock": ["led zeppelin", "queen", "acdc", "classic rock"],
    "pop": ["taylor swift", "britney spears", "justin bieber"],
}

def detect_genre(title):
    title_lower = title.lower()
    for genre, keywords in GENRE_KEYWORDS.items():
        if any(re.search(rf"\b{k}\b", title_lower) for k in keywords):
            return genre
    return "unknown"