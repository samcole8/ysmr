"""Handle inputs from logstash and pass them to notification modules."""

import argparse
import importlib
import os
import sys

import toml

# Path to configuration file
MODULE_PATH = "/../modules/"
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

    def __init__(self, timestamp=None, **kwargs):
        self.timestamp = timestamp
        self.other = kwargs

class SSHLog(Log):
    """SSH log child class."""

    def __init__(self, status=None, ipv4=None, port=None, **kwargs):
        super().__init__(**kwargs)
        self.type = "SSH"
        self.status = status
        self.ipv4 = ipv4
        self.port = port

    def get_msg(self):
        """Generate human-readable message for SSH log information."""
        message_parts = [self.type]

        # Add status to message
        if self.status:
            message_parts.append(f"login {self.status}")
        else:
            message_parts.append("authentication activity")
        # Add IPv4 address to message
        if self.ipv4:
            message_parts.append(f"from {self.ipv4}")
        # Add port to message
        if self.port:
            message_parts.append(f"on port {self.port}")
        # Add port to message
        if self.timestamp:
            message_parts.append(f"at {self.timestamp}")

        # Construct final message
        message = " ".join(message_parts) + "."

        return message

def load_config(path):
    """Open config and return object list."""
    try:
        with open(path) as f:
            # Create config object
            config = Config()
            # Create config module objects
            try:
                config.modules = [
                    config.Module(**module)
                    for module in toml.load(f).get('module', [])
                    if module.get('enabled', False)
                ]
            except TypeError as e:
                sys.exit(f"ysmr.py: error: Configuration is invalid:\n{e}")
    except FileNotFoundError:
        sys.exit(f"ysmr.py: error: {path} does not exist.")
        raise
    except PermissionError:
        sys.exit(f"ysmr.py: error: Permission denied for {path}.")
        raise
    return config

def ysmr(log):
    """Pass parameters to notification modules."""
    # Add directory containing this script to the Python module search path
    script_dir = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(script_dir + MODULE_PATH)
    # Load config objects
    config = load_config(CONFIG_PATH)
    # Run module, pass config & log
    for module in config.modules:
        try:
            # Dynamically import module
            importlib_module = importlib.import_module(module.name)
            # Catch-all for module exceptions
            try:
                importlib_module.run(module, log)
            except Exception as e:
                print(f"{module.name}: error: {e}")
        except ModuleNotFoundError:
            print(f"ysmr.py: error: module {module.name} could not be "
                  "imported. Is it in the project folder?")

def parse():
    """Use argparse to parse command-line arguments.

    Create log object from CLI arguments.
    """
    # Create parsers
    parser = argparse.ArgumentParser(description='Process arguments.')
    subparsers = parser.add_subparsers(title='functions', dest='subcommand')
    ssh_parser = subparsers.add_parser('ssh', help='SSH notification')

    # Optional arguments for SSH
    ssh_parser.add_argument("--timestamp",
                            type=str,
                            default=None,
                            help="specify timestamp")
    ssh_parser.add_argument("--status",
                            type=str,
                            default=None,
                            help="specify status")
    ssh_parser.add_argument("--ipv4",
                            type=str,
                            default=None,
                            help="specify IPv4 address")
    ssh_parser.add_argument("--port",
                            type=str,
                            default=None,
                            help="specify port number")

    # Parse arguments
    args = parser.parse_args()

    # Check if subcommand is provided and handle accordingly
    if args.subcommand == 'ssh':
        # Create SSHLog object using provided arguments
        log = SSHLog(timestamp=args.timestamp,
                     status=args.status,
                     ipv4=args.ipv4,
                     port=args.port)
    else:
        sys.exit("ysmr.py: error: Log type is invalid or not specified")

    # Return log object
    return log

if __name__ == "__main__":
    ysmr(parse())
