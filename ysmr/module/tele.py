import helpers

CONFIG = "modules/tele.conf"

def get_url(endpoint):
    """Get bot URL"""
    return f"https://api.telegram.org/bot{endpoint[1]}/sendMessage"

def get_params(endpoint, payload):
    """Generate text from payload data."""
    status = {0:"Failed", 1:"Successful"}
    text = f"{status[payload[2]]} login from {payload[0]} on port {payload[1]}."
    return {"chat_id": endpoint[0], "text": text}

def wrap(endpoint, payload):
    """Return API call for specified payload."""
    absolute_path = helpers.get_path()
    return [(get_url(endpoint), get_params(endpoint, payload))]