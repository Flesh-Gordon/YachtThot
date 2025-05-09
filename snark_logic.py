# snark_logic.py

import random
from snark_pool import get_snark_reply, get_no_result_snark

EXEMPT_USERS = ["sdevil713"]
SNARKY_GENRES = ["bro-country", "hyperpop", "eurodance"]
SNARK_PROBABILITY = 0.25

def maybe_add_snark(username, genre, is_dedication=False, song_found=True, is_repeat=False):
    if username.lower() in EXEMPT_USERS:
        return ""

    # Always snark dedications
    if is_dedication:
        return get_snark_reply()

    # If song wasn't found, 25% chance of snark
    if not song_found:
        return get_no_result_snark() if random.random() < SNARK_PROBABILITY else ""

    # Trigger snark on repeat or genre with 25% chance
    if is_repeat or (genre and genre.lower() in SNARKY_GENRES):
        if random.random() < SNARK_PROBABILITY:
            return get_snark_reply()

    # 25% general snark chance
    if random.random() < SNARK_PROBABILITY:
        return get_snark_reply()

    return ""