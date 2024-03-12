"""Handle inputs from logstash and pass them to notification modules."""

import toml
import sys

# Relative path to configuration file
CONFIG_PATH = "ysmr.toml"

def load_config():
    """Open config and return dictionary"""
    with open(CONFIG_PATH, "r") as f:
        config = toml.load(f)
    return config

def yssh(time, status, ipv4, port):
    """Pass parameters to notification modules."""
    config = load_config()


if __name__ == "__main__":
    yssh(sys.argv[0], sys.argv[1], sys.argv[2], sys.argv[4])