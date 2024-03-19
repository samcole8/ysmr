"""Initialisation file for modules package."""


from dataclasses import dataclass


class Module:
    """Module superclass."""

    def __init__(self, log, instances):
        """Initialise Module class."""
        self.log = log
        # Create Instance objects from conf
        self.instances = [
            self.Instance(**instance)
            for instance in instances
            if instance.get("enabled")
        ]

    @dataclass
    class Instance:
        """Parent Instance class to be inherited."""

        pass

    def notify(self):
        """Wrap notification code in error check."""
        for instance in self.instances:
            try:
                instance.go(self.log)
            except AttributeError as e:
                print(f"Check YourModule.send() for errors: {e}")
            except Exception as e:
                print(f"Exception occured: {e}")
