"""MongoDB notification module for ysmr.

This module accepts the log and instig objects created by ysmr.

Using API parameters provided in the instig object, the log data is
wrapped in an API call and sent to MongoDB accordingly.

This module is packaged by default with ysmr.
"""

from pymongo import MongoClient


def run(inst, log):
    """Send MongoDB data."""
    # Create document from log data
    document = {}
    for key, value in vars(log).items():
        document[key] = value
    # Open MongoDB connection and post data
    with MongoClient(inst.url) as client:
        db = client[inst.db]
        collection = db[inst.collection]
        collection.insert_one(document)
