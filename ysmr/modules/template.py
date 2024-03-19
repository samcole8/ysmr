"""Template module file."""

# Module-specific imports here

# Required imports
from . import Module, dataclass


class MyModule(Module):
    """Custom module class.

    This class can store attributes and send methods for custom modules. You
    can rename it.

    It must contain at least an `Instance` class and `go` method, as below.
    """

    @dataclass
    class Instance(Module.Instance):
        """Dataclass for defining configuration attributes."""

        # Define your attributes here
        my_attribute_1: str
        my_attribute_2: int
        my_attribute_3: bool

        def go(self):
            """Deposit/send data in the specified method."""
            # Add your notification code here
            print(self.my_attribute_1)
