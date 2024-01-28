import requests
from importlib import import_module
import sys

import helpers

CONFIG = "ysmr.toml" # Relative path to config

def get_payload():
    """Get payload from command line arguments"""
    return (ip:=str(sys.argv[1]),
            port:=int(sys.argv[2]),
            status:=int(sys.argv[3]))

def post(calls):
    """Post API calls"""
    if len(calls) != 0:
        for call in calls:
            post = requests.post(call[0], params=call[1])
        
    else:
        print("No calls were sent. Are any modules loaded?")

def call_gen(config, payload):
    """Generate API calls from payload"""
    calls = []
    # For every module in config file
    for mod_name, mod_config in config["module"].items():
        if mod_config["enabled"] is True:
            mod = import_module("module." + mod_name)
            for endpoint in mod_config["endpoint"].values():
                calls += mod.wrap(endpoint, payload)
    return calls

def ysmr():
    """Craft and post API calls."""
    # Get absolute path and load config file
    absolute_path = helpers.get_path()
    config = helpers.load_toml(absolute_path / CONFIG)
    payload = get_payload()
    if config["ysmr"]["enabled"] is True:
        calls = call_gen(config, payload)
        post(calls)
    else:
        print("[ysmr]: Script is disabled.")

if __name__ == "__main__":
    ysmr()
