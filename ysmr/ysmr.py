"""Handle inputs and pass them to notification modules."""

import argparse
import importlib
import os
import sys

import toml

# Path to configuration file
MODULE_PATH = "modules/"
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "ysmr.toml")

class Config:
    """Config class."""

    def __init__(self, data):
        """Initialise new instance of the Config class.

        This method initialises the Config object by loading module data
        from the provided dictionary into objects.

        Args:
        ----
            data (dict): Dictionary containing configuration data, typically
                loaded from a configuration file.

        """
        # Create Module objects and load into self
        self.modules = [self.Module(**data) for data in data["module"]]


    class Module:
        """Module configuration class.

        Config modules refer to any notification module (SMS, smtp e.t.c.).
        """

        def __init__(self, name, enabled, instance, **kwargs):
            """Initialise new instance of the Module class.

            This method initialises the Module object by loading instance data
            from the provided dictionary.

            Args:
            ----
                name (string): Name of the module.

                enabled (bool): Is the module enabled?

                instance (dict): Instance data from configuration file.

                **kwargs (*): Additional user-defined parameters.

            """
            # Initialise Module attributes
            self.name = name
            self.enabled = enabled
            # Create Instance objects and load into self
            self.instances = [self.Instance(**data) for data in instance]

        def is_enabled(self):
            """Return value based on enabled attribute."""
            return self.enabled

        class Instance:
            """Instance configuration class.

            Instances are individual accounts or notification endpoints.
            """

            def __init__(self, name, enabled, **kwargs):
                """Initialise new object from Instance class.

                Args:
                ----
                    name (string): Name of the module.

                    enabled (bool): Is instance enabled?

                    **kwargs (*): Any dynamic options required by
                    module-specific functions.

                """
                # Initialise static attributes
                self.name = name
                self.enabled = enabled
                # Initialise dynamic attributes
                for key, value in kwargs.items():
                    setattr(self, key, value)

            def is_enabled(self):
                """Return value based on enabled attribute."""
                return self.enabled

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

def load_config(path):
    """Open config and return object list."""

    def read_file(path):
        try:
            with open(path) as f:
                toml_data = toml.load(f)
        except FileNotFoundError:
            sys.exit(f"ysmr.py: error: {path} does not exist.")
        except PermissionError:
            sys.exit(f"ysmr.py: error: Permission denied for {path}.")
        return toml_data

    def create_object(config_data):
        # Create config object
        try:
            config = Config(config_data)
        except (TypeError) as e:
            sys.exit(f"ysmr.py: error: Configuration is invalid:\n{e}")
        except (KeyError) as e:
            sys.exit(f"ysmr.py: error: KeyError occured when loading"
            f" configuration:\nKey:{e}.")
        return config

    toml_data = read_file(path)
    config = create_object(toml_data)
    return config

def ysmr(log):
    """Pass parameters to notification modules."""
    # Add directory containing this script to the Python module search path
    script_dir = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(script_dir + "/" + MODULE_PATH)

    # Load config objects
    try:
        config = load_config(CONFIG_PATH)
    except toml.TomlDecodeError as e:
        print(f"ysmr.py: error: Invalid Toml syntax in config:\n{e}")
        sys.exit()

    # Run each module
    for module in config.modules:
        if module.is_enabled():
            try:
                # Dynamically import module
                importlib_module = importlib.import_module(module.name)
                # Run each instance
                for instance in module.instances:
                    if instance.is_enabled():
                        # Catch-all for module exceptions
                        try:
                            importlib_module.run(instance, log)
                        except Exception as e:
                            print(f"{module.name}: error: {e}")
            except ModuleNotFoundError:
                print(f"ysmr.py: error: module {module.name} could not be "
                    "imported. Is it in the project folder?")

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
