"""Handle inputs from logstash and pass them to notification modules."""

import toml
import importlib
import argparse

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
        module_configs = [
            ModuleConfig(**module_config)
            for module_config in toml.load(f).get('module', [])
            if module_config.get('enabled', False)
        ]
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
        try:
            module.run(module_config, log)
        except Exception as e:
            print(f"ERROR: Exception occured in {module_config.name} module:\n{e}")

def parse():
    # Create ArgumentParser object
    parser = argparse.ArgumentParser(description='Process some strings.')

    # Add timestamp argument
    parser.add_argument("timestamp", type=str,
                        help="timestamp string")

    # Add flag for SSH options
    ssh_group = parser.add_argument_group("SSH options")
    ssh_group.add_argument("--ssh", action="store_true",
                           help='enable SSH options')
    ssh_group.add_argument("--status", type=str, default="",
                           help="status string (required for SSH)")
    ssh_group.add_argument("--ipv4", type=str, default="",
                           help="IPv4 address string (required for SSH)")
    ssh_group.add_argument("--port", type=str, default="",
                           help="port string (required for SSH)")

    # Parse arguments
    args = parser.parse_args()

    # Check if SSH options are provided when --ssh flag is used
    if args.ssh and (not args.status or not args.ipv4 or not args.port):
        parser.error("--status, --ipv4, and --port are required with --ssh")

    return args.timestamp, args.status, args.ipv4, args.port

if __name__ == "__main__":
    ysmr(*parse())