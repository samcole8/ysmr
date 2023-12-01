import helpers

CONFIG = "ysmr.conf" # Relative path to config

def parse():
    return 0

def ysmr():
    """Parse SSH log for latest data and post to API."""
    absolute_path = helpers.get_path()
    config = helpers.load_json(CONFIG)
    # Open log and parse for data.
    with open(absolute_path / config["log_path"]) as ssh_log:
        payload = parse(ssh_log)

if __name__ == "__main__":
    ysmr()