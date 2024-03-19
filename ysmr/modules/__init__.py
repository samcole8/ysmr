"""Initialisation file for modules package."""


from dataclasses import dataclass


class Module:
    """Parent Module class to be inherited."""

    def __init__(self, log, conf):
        """Initialise Module class."""
        self.log = log
        # Create Instance objects from conf
        self.instances = [
            self.Instance(**inst_data)
            for inst_data in conf["instance"]
        ]

    @dataclass
    class Instance:
        """Parent Instance class to be inherited."""

        pass
