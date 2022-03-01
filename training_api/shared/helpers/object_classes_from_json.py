import json

from typing import Dict

"""
creates a dict of ids and names from the objectclasses.json file

Returns
-------
dict
	labels id mapped to label name

"""


def get_labels_from_json_file(json_input) -> Dict[str, str]:
    json_file_labels = json.load(open(json_input, "rb"))
    i = 1
    labels: Dict[str, str] = {}
    for label in json_file_labels:
        labels[str(i)] = label["Name"]
        i += 1
    return labels
