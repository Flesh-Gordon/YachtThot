# dedication_tracker.py

import re

def extract_dedication(text):
    match = re.search(r"dedicated to u/(\w+)", text, re.IGNORECASE)
    if match:
        return match.group(1)
    return None