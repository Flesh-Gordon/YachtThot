snark_data = {
    "repeat": [
        "Again? You playing this like it’s a one-track mind.",
        "Didn’t you request this already? We heard you the first time.",
        "Somebody's stuck in a loop. Try a new song for once.",
        "Back at it with the reruns, huh?"
    ],
    "cringe": [
        "Bold choice. I’ll give you that.",
        "This better be a joke. If not… yikes.",
        "You really woke up and picked *this*?",
        "Audacity is free, and you clearly stocked up."
    ],
    "banger": [
        "Certified. Absolute heat.",
        "Taste. Real recognize real.",
        "Now that’s how you do it. Respect.",
        "Banger detected — you may proceed."
    ],
    "tagline": [
        "We now return to your regularly scheduled clown show.",
        "This song choice brought to you by a complete lack of shame.",
        "Not even ChatGPT can save your taste.",
        "Imagine thinking this was the move… and then hitting ‘submit’."
    ],
    "dedication": [
        "Nothing says ‘I care’ like weaponized music.",
        "A dedication? That’s either sweet or wildly passive-aggressive.",
        "Sending this track like a digital middle finger. We see you.",
        "Is this love, a threat, or both?"
    ],
    "gay_anthem": [
        "YachtThot detected maximum pride levels. Fabulous.",
        "Slay. Wig gone. Floor stomped. It’s giving ICON.",
        "We’re serving looks and tracks — let’s go queens.",
        "This playlist is now 200% more fierce."
    ]
}

def get_snark_reply(category: str) -> str:
    import random
    return random.choice(snark_data.get(category, ["No snark available."]))
