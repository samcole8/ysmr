"""Mongo (MongoDB) module for ysmr.

This module is packaged by default with ysmr.
"""

from pymongo import MongoClient

from . import Module, dataclass

class Mongo(Module):

    @dataclass
    class Instance(Module.Instance):
        name: str
        enabled: bool
        url: str
        db: str
        collection: str

    def go(self, instance):
        """Send MongoDB data."""
        # Create document from log data
        document = {}
        for key, value in vars(self.log).items():
            document[key] = value

        # Open MongoDB connection and post data
        with MongoClient(instance.url) as client:
            db = client[instance.db]
            collection = db[instance.collection]
            print(collection.insert_one(document))
