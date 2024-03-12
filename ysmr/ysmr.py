"""Handle inputs from logstash and pass them to notification modules."""

import toml
import sys

# Relative path to configuration file
CONFIG_PATH = "ysmr.toml"

class Module:
    def __init__(self, name, **kwargs):
        self.name = name
        self.settings = kwargs

def load_config():
    """Open config and return dictionary"""
    with open(CONFIG_PATH, "r") as f:
        config = toml.load(f)
    return config

def ysmr(timestamp, status, ipv4, port):
    """Pass parameters to notification modules."""
    config = load_config()
    # Create list of enabled Module instances
    modules = [Module(**module) for module in config.get('module', []) if module.get('enabled', False)]

if __name__ == "__main__":
    ysmr(sys.argv[0], sys.argv[1], sys.argv[2], sys.argv[4])