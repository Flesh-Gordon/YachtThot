# snark_pool.py

snark_replies = [
    "Oh, this again? Your taste in music hasn't improved.",
    "You sure you want the world to know you like this?",
    "Not again... even the algorithm groaned.",
    "You're really testing the limits of my patience with this one.",
    "Back at it with another chart-topper of cringe, huh?",
    "This one's a certified vibe-killer.",
    "Every time you request this, a headphone dies somewhere.",
    "That genre again? You're nothing if not consistent...ly awful.",
    "If bad taste were a crime, you'd be serving life.",
    "I’d roast you harder, but I’m saving bandwidth."
]

no_result_snark = [
    "Not even YouTube could save that request.",
    "You made me look for *what* now?",
    "Whatever that was... it shouldn't exist.",
    "You really think that was a song?",
    "This request was so bad, even the internet said no."
]

def get_snark_reply():
    import random
    return random.choice(snark_replies)

def get_no_result_snark():
    import random
    return random.choice(no_result_snark)