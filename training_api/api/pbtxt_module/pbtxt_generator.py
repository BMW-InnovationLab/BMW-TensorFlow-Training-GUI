from utils.labelingtool_utils.object_classes_handler import get_labels_from_json_file


"""
gets the label names from the objectclasses.json file and converts them to pbtxt file

"""

def generate_pbtxt():
	labels = get_labels_from_json_file('/dataset/objectclasses.json')
	f = open('/training_dir/data/object-detection.pbtxt','w+')	
	for key,value in labels.items():
		f.write('item { \n')
		f.write('  id: ' + key + '\n')
		f.write('  name: "' + value + '"\n')
		f.write("} \n")
	f.close()