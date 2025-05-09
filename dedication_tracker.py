import re

def extract_dedication(text):
    """
    Detects if a request is a dedication like 'dedicated to u/username'
    Returns (is_dedication, target_user) — fallback to (False, None)
    """
    match = re.search(r"dedicated to u/(\w+)", text, re.IGNORECASE)
    if match:
        return True, match.group(1)
    return False, None