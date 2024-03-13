"""Handle inputs from logstash and pass them to notification modules."""

import toml
import sys
import importlib

# Relative path to configuration file
CONFIG_PATH = "ysmr.toml"

class ModuleConfig:
    def __init__(self, name, enabled, **kwargs):
        self.name = name
        self.enabled = enabled
        for key, value in kwargs.items():
            setattr(self, key, value)

class Log:
    def __init__(self, timestamp, **kwargs):
        self.timestamp = timestamp
        self.other = kwargs

class SSHLog(Log):
    def __init__(self, status, ipv4, port, **kwargs):
        super().__init__(**kwargs)
        self.status = status
        self.ipv4 = ipv4
        self.port = port

def load_config(path):
    """Open config and return object list"""
    with open(path, "r") as f:
        # Create list of enabled Module instances
        module_configs = [ModuleConfig(**module_config) for module_config in toml.load(f).get('module', []) if module_config.get('enabled', False)]
    return module_configs

def ysmr(timestamp, status, ipv4, port):
    """Pass parameters to notification modules."""
    # Create SSHLog object
    log = SSHLog(timestamp=timestamp, status=status, ipv4=ipv4, port=port)
    # Load config objects
    module_configs = load_config(CONFIG_PATH)
    # Run module, pass config & log
    for module_config in module_configs:
        module = importlib.import_module(module_config.name)
        module.run(module_config, log)
        

if __name__ == "__main__":
    ysmr(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])