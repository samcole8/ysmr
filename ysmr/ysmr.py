"""Handle inputs from logstash and pass them to notification modules."""

import toml
import sys
import importlib

# Relative path to configuration file
CONFIG_PATH = "ysmr.toml"

class Log:
    def __init__(self, timestamp, **kwargs):
        self.timestamp = timestamp
        self.other = kwargs

class SSHLog(Log):  # SSHLog inherits from Log
    def __init__(self, status, ipv4, port, **kwargs):
        # Call the __init__ method of the base class (Log) using super()
        super().__init__(**kwargs)
        self.status = status
        self.ipv4 = ipv4
        self.port = port

class Module:
    def __init__(self, name, enabled, **kwargs):
        self.name = name
        self.settings = kwargs

def load_config():
    """Open config and return dictionary"""
    with open(CONFIG_PATH, "r") as f:
        config = toml.load(f)
    return config

def ysmr(timestamp, status, ipv4, port):
    """Pass parameters to notification modules."""
    log = SSHLog(timestamp=timestamp, status=status, ipv4=ipv4, port=port)
    config = load_config()
    # Create list of enabled Module instances
    modules = [Module(**module) for module in config.get('module', []) if module.get('enabled', False)]
    for module in modules:
        mod = importlib.import_module(module.name)
        mod.run(module.settings, log)
        

if __name__ == "__main__":
    ysmr(sys.argv[0], sys.argv[1], sys.argv[2], sys.argv[4])