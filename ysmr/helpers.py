import json
from pathlib import Path
import toml
import datetime

def log(config, message):
    if config["ysmr"]["log"] == True:
        with open("ysmr.log", "a") as log:
            log.write(str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + " " + message + "\n")

def load_toml(path):
    """Open TOML file and return dictionary"""
    with open(path, "r") as toml_file:
        toml_dict = toml.load(toml_file)
    return toml_dict

def load_json(path):
    """Open JSON file and return dictionary"""
    with open(path, "r") as json_file:
        json_dict = json.load(json_file)
    return json_dict

def get_path():
    """Return absolute file path"""
    return Path(__file__).parent
