"""Handle inputs and pass them to notification modules."""

import argparse
import os
import sys

import toml

# Path to configuration file
MODULE_PATH = "modules/"
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "ysmr.toml")

class Log:
    """Template log class."""

    def __init__(self, timestamp=None, **kwargs):
        """Initialise a new instance of the Log class.

        Sets timestamp attribute, and adds any unexpected parameters to other
        dictionary.
        """
        self.timestamp = timestamp

class SSHLog(Log):
    """SSH log child class."""

    def __init__(self, status=None, ipv4=None, port=None, **kwargs):
        """Initialise a new instance of the SSHLog child class.

        If provided, assigns expected arguments to the correct attributes.
        """
        super().__init__(**kwargs)
        self.type = "SSH"
        self.status = status
        self.ipv4 = ipv4
        self.port = port

    def get_msg(self):
        """Generate human-readable message for SSH log information."""
        message_parts = [self.type]

        # Dynamically add items to message_parts
        if self.status:
            message_parts.append(f"login {self.status}")
        else:
            message_parts.append("authentication activity")
        if self.ipv4:
            message_parts.append(f"from {self.ipv4}")
        if self.port:
            message_parts.append(f"on port {self.port}")
        if self.timestamp:
            message_parts.append(f"at {self.timestamp}")

        # Construct message
        message = " ".join(message_parts) + "."
        return message

def load_toml(path):
    """Open TOML file and return dictionary object."""
    try:
        with open(path) as f:
            toml_data = toml.load(f)
    except FileNotFoundError:
        sys.exit(f"ysmr.py: error: {path} does not exist.")
    except PermissionError:
        sys.exit(f"ysmr.py: error: Permission denied for {path}.")
    return toml_data

def ysmr(log):
    config = load_toml(CONFIG_PATH)
    pass

def parse_arguments():
    """Parse CLI arguments into Log instance."""
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

    if args.subcommand == 'ssh':
        # Create SSHLog object using arguments, where provided
        log = SSHLog(timestamp=args.timestamp,
                     status=args.status,
                     ipv4=args.ipv4,
                     port=args.port)
    else:
        sys.exit("ysmr.py: error: Log type is invalid or not specified")

    return log

if __name__ == "__main__":
    ysmr(parse_arguments())
