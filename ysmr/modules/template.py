"""Template module file."""

# Module-specific imports here

# Required imports
from . import Module, dataclass

class MyModule(Module):

    @dataclass
    class Instance(Module.Instance):
        # Define your attributes here
        my_attribute_1: str
        my_attribute_2: int
        my_attribute_3: bool

    def send(self):
        # Add your notification code here
        pass