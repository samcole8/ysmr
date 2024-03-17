"""MongoDB notification module for ysmr.

This module accepts the log and config objects created by ysmr.

Using API parameters provided in the config object, the log data is
wrapped in an API call and sent to MongoDB accordingly.

This module is packaged by default with ysmr.
"""

from pymongo import MongoClient


def run(conf, log):
    """Send MongoDB data."""
    # Create document from log data
    document = {}
    for key, value in vars(log).items():
        document[key] = value
    # Open MongoDB connection and post data
    with MongoClient(conf.url) as client:
        db = client[conf.db]
        collection = db[conf.collection]
        collection.insert_one(document)
