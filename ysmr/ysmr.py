"""Handle inputs from logstash and pass them to notification modules."""

import argparse
import importlib
import os
import sys

import toml

# Path to configuration file
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "ysmr.toml")

class Config:
    """Config class."""

    def __init__(self):
        self.modules = []

    class Module:
        """Module configuration class."""

        def __init__(self, name, enabled, **kwargs):
            self.name = name
            self.enabled = enabled
            for key, value in kwargs.items():
                setattr(self, key, value)

class Log:
    """Template log class."""

    def __init__(self, timestamp, **kwargs):
        self.timestamp = timestamp
        self.other = kwargs

class SSHLog(Log):
    """SSH log child class."""

    def __init__(self, status=None, ipv4=None, port=None, **kwargs):
        super().__init__(**kwargs)
        self.status = status
        self.ipv4 = ipv4
        self.port = port

    def get_msg(self):
        """Generate human-readable message for SSH log information."""
        message_parts = []

        # Add status to message
        if self.status:
            message_parts.append(f"{self.status} login")

        # Add IPv4 address to message
        if self.ipv4:
            message_parts.append(f"from {self.ipv4}")

        # Add port to message
        if self.port:
            message_parts.append(f"on port {self.port}")

        # Construct final message
        if message_parts:
            message = " ".join(message_parts) + "."
        else:
            message = "SSH activity detected."

        return message

def load_config(path):
    """Open config and return object list."""
    with open(path) as f:
        # Create config object
        config = Config()
        # Create config module objects
        config.modules = [
            config.Module(**module)
            for module in toml.load(f).get('module', [])
            if module.get('enabled', False)
        ]
    return config

def ysmr(timestamp, status, ipv4, port):
    """Pass parameters to notification modules."""
    # Create SSHLog object
    log = SSHLog(timestamp=timestamp, status=status, ipv4=ipv4, port=port)
    # Load config objects
    config = load_config(CONFIG_PATH)
    # Run module, pass config & log
    for module in config.modules:
        importlib_module = importlib.import_module(module.name)
        try:
            importlib_module.run(module, log)
        except Exception as e:
            print(f"ERROR: Exception occured in {module.name} module:"
                  f"\n{e}")

def parse():
    """Use argparse to parse command-line arguments."""
    # Create ArgumentParser object
    parser = argparse.ArgumentParser(description='Process some strings.')

    # Add timestamp argument
    parser.add_argument("timestamp", type=str,
                        help="timestamp string")

    # SSH group
    ssh_group = parser.add_argument_group("SSH options")
    # Set args
    ssh_arguments = {
        "--ssh": {"action": "store_true",
                  "help": "specify SSH log type"},
        "--status": {"type": str,
                     "default": "",
                     "help": "status string (required for SSH)"},
        "--ipv4": {"type": str,
                   "default": "",
                   "help": "IPv4 address string (required for SSH)"},
        "--port": {"type": str,
                   "default": "",
                   "help": "port string (required for SSH)"}
    }
    # Add arguments
    for arg, config in ssh_arguments.items():
        ssh_group.add_argument(arg, **config)

    # Parse arguments
    args = parser.parse_args()

    return args.timestamp, args.status, args.ipv4, args.port

if __name__ == "__main__":
    # Add directory containing this script to the Python module search path
    script_dir = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(script_dir)
    ysmr(*parse())
