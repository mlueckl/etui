import json

def is_json(t):
    try:
        _ = json.loads(t)
        return True
    except ValueError:
        return False
