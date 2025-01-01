import json


def is_json(s: str) -> bool:
    """Validate if input is a valid JSON-string

    Args:
        s (str): Input string

    Returns:
        bool: Is valid
    """
    try:
        _ = json.loads(s)
        return True
    except (ValueError, TypeError):
        return False
