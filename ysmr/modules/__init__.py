"""Initialisation file for modules package."""


from dataclasses import dataclass


class Module:
    """Module superclass."""

    def __init__(self, log, conf):
        """Initialise Module class."""
        self.log = log
        # Create Instance objects from conf
        self.instances = [
            self.Instance(**inst_data)
            for inst_data in conf["instance"]
            if inst_data.get("enabled")
        ]

    @dataclass
    class Instance:
        """Parent Instance class to be inherited."""

        pass
