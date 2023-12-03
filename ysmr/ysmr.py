import datetime
import requests
import importlib

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

def post(url, params):
    post = requests.post(url, params=params)
    print(post)

def ysmr():
    """Parse SSH log for latest data and post to API."""
    absolute_path = helpers.get_path()
    config = helpers.load_json(absolute_path / CONFIG)
    # Open log and parse for data.
    with open(absolute_path / config["ssh_log_path"]) as ssh_log:
        ssh_log = ssh_log.readlines()
    payload = parse(ssh_log)
    # Post API call for each active module.
    for module in config["modules"]:
        if config["modules"][module] == "1":
            # Import modules temporarily to get API calls.
            temp_module = importlib.import_module("modules." + module)
            call_list = temp_module.wrap(payload)
            # Post API calls.
            for call in call_list:
                url = call[0]
                params = call[1]
                post(url, params)


if __name__ == "__main__":
    ysmr()