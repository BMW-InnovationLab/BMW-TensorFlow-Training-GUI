import json
import io


"""
creates a dict of ids and names from the objectclasses.json file

Returns
-------
dict
	labels id mapped to label name

"""

def get_labels_from_json_file(json_input):
	# json_file_labels = json.loads(io.open(json_input,"r", encoding='utf-16').read())
	json_file_labels = json.load(open(json_input, "rb"))
	i = 1
	labels = {}
	for label in json_file_labels:
		labels[str(i)] = label["Name"]
		i += 1
	return labels

		



