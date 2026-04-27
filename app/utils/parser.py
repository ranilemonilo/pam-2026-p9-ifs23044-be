import json
import re

def parse_recipes_from_text(text: str) -> list:
    """
    Parse AI-generated recipe JSON from text response.
    Returns list of recipe dicts.
    """
    # Try to extract JSON array from the response
    json_match = re.search(r'\[.*\]', text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass

    # Fallback: try direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return []