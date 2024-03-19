"""Initialisation file for modules package."""


from dataclasses import dataclass


class Module:
    """Module superclass."""

    def __init__(self, name, enabled, log, instance):
        """Initialise Module class."""
        self.name = name
        self.enabled = enabled
        self.log = log
        # Create Instance objects from conf
        self.instances = [
            self.Instance(**instance)
            for instance in instance
            if instance["enabled"]
        ]

    @dataclass
    class Instance:
        """Parent Instance class to be inherited."""

        pass

    def notify(self):
        """Wrap notification code in error check."""
        for instance in self.instances:
            try:
                self.go(instance)
            except AttributeError as e:
                print(f"Check YourModule.send() for errors: {e}")
            except Exception as e:
                print(f"Exception occured: {e}")
