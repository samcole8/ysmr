import json
from pathlib import Path

def load_json(path):
    """Open JSON file and return dictionary"""
    with open(path, "r") as json_file:
        json_dict = json.load(json_file)
    return json_dict

def get_path():
    """Return absolute file path"""
    return Path(__file__).parent

def convert_to_text(payload):
    if payload["type"] == "1":
        return f"Accepted login for '{payload['name']}' from {payload['ipv4']} ({payload['hour']}:{payload['minute']}:{payload['second']})"
    return f"Rejected login for '{payload['name']}' from {payload['ipv4']} ({payload['hour']}:{payload['minute']}:{payload['second']})"