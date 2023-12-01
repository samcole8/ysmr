import datetime

import helpers

CONFIG = "ysmr.conf" # Relative path to config

def parse(ssh_log):
    """Filter SSH log for relevant data."""
    # Define payload template
    payload = {
        "type":"",
        "year":"",
        "day":"",
        "hour":"",
        "minute":"",
        "second":"",
        "ipv4":"",
        "name":"",
        "port":""
    }
    ssh_log_chron = reversed(ssh_log.readlines()) # Make log iterable in chronological order
    for line in ssh_log_chron:
        # If line is relevant:
        if "password" in line:
            print(line)
            # Set payload values
            if "Accepted" in line:
                payload_type = "1"
            else:
                payload_type = "0"
            lexemes = line.split(" ")
            time_split = lexemes[2].split(":")
            payload["type"] = payload_type
            payload["year"] = datetime.datetime.now().year
            payload["day"] = lexemes[1]
            payload["hour"] = time_split[0]
            payload["minute"] = time_split[1]
            payload["second"] = time_split[2]
            payload["ipv4"] = lexemes[10]
            payload["name"] = lexemes[8]
            payload["port"] = lexemes[12]
            break
    return payload

def ysmr():
    """Parse SSH log for latest data and post to API."""
    absolute_path = helpers.get_path()
    config = helpers.load_json(CONFIG)
    # Open log and parse for data.
    with open(absolute_path / config["ssh_log_path"]) as ssh_log:
        payload = parse(ssh_log)
    print(payload)

if __name__ == "__main__":
    ysmr()