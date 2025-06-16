import re

def extract_place_query(user_input: str) -> tuple:
    """
    Extracts place type and location from user input.
    E.g., "Find coffee shops near Palo Alto" → ("coffee shop", "Palo Alto")
    """
    pattern = r"(?:find|show|recommend|search|look for)?\s*(.*?)\s+(?:near|around|in)\s+(.*)"
    match = re.search(pattern, user_input, re.IGNORECASE)
    if match:
        place_type = match.group(1).strip()
        location = match.group(2).strip()
        return place_type, location
    return None, None
