import requests
import importlib
from elasticsearch import Elasticsearch

import helpers

CONFIG = "ysmr.conf" # Relative path to config

def post(url, params):
    post = requests.post(url, params=params)
    print(post)

def fetch(port, host, index):
    es = Elasticsearch(f"{host}:{port}")
    query = {
        "query": {
            "match_all": {}
        }
    }
    result = es.search(index=index, body=query)
    for hit in result['hits']['hits']:
        print(hit['_source'])
    es.close()


def ysmr():
    """Parse SSH log for latest data and post to API."""
    absolute_path = helpers.get_path()
    config = helpers.load_json(absolute_path / CONFIG)
    # Open log and get data
    fetch(config["port"], config["host"], config["index"])
    # Post API call for each active module.
#    for module in config["modules"]:
#        if config["modules"][module] == "1":
#            # Import modules temporarily to get API calls.
#            temp_module = importlib.import_module("modules." + module)
#            call_list = temp_module.wrap(payload)
#            # Post API calls.
#            for call in call_list:
#                url = call[0]
#                params = call[1]
#                post(url, params)


if __name__ == "__main__":
    ysmr()