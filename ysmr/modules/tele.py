import helpers

CONFIG = "modules/tele.conf"

def get_url(config):
    return f"https://api.telegram.org/bot{config['token']}/sendMessage"

def get_params(payload, config):
    return {"chat_id": config["id"], "text": helpers.convert_to_text(payload)}

def wrap(payload):
    absolute_path = helpers.get_path()
    config = helpers.load_json(absolute_path / CONFIG)
    return [(get_url(config), get_params(payload, config))]