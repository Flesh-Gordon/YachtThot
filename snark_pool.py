import random

GENERIC_SNARK = [
    "Bold choice. I respect the lack of shame.",
    "If cringe was a genre, this would top the charts.",
    "Ah yes, the sonic equivalent of a face tattoo.",
    "You’ve got the musical taste of a drunk algorithm.",
    "Was this playing during your last bad decision?"
]

REPEAT_SNARK = [
    "Back at it with this track again? Obsession is a hell of a thing.",
    "You’ve played this so much it’s filing taxes.",
    "Even Spotify thinks you need therapy.",
    "This song again? Let it go, Elsa.",
    "Repetition is the sincerest form of musical insanity."
]

GENRE_SNARK = {
    "country": [
        "Nothing like a banjo to say, ‘I’ve given up.’",
        "Your truck must be crying right now.",
    ],
    "pop": [
        "Pop: because you fear introspection.",
        "Sweet, catchy, and utterly devoid of substance. Just like your ex."
    ],
    "metal": [
        "Ah, metal. Screaming because talking it out was too mainstream.",
        "This song bench presses more than you do."
    ],
    "rap": [
        "Rap game strong, but your taste? Debatable.",
        "Another lyrical masterpiece about money, cars, and... feelings?"
    ],
    "edm": [
        "EDM: when your playlist needs more glow sticks and fewer brain cells.",
        "The beat drops harder than your GPA."
    ]
}

def get_snark(context=None, genre=None, repeat=False):
    snarks = []

    if repeat:
        snarks += REPEAT_SNARK
    elif genre and genre.lower() in GENRE_SNARK:
        snarks += GENRE_SNARK[genre.lower()]
    else:
        snarks += GENERIC_SNARK

    return random.choice(snarks) if snarks and random.random() < 0.25 else ""
