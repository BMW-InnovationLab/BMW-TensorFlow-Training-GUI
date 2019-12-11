import os
import json

basedir = os.getcwd()
paths_json = json.loads(open("docker_sdk_api/api/paths.json", "r").read())
paths_json["base_dir"] = basedir

with open('docker_sdk_api/api/paths.json', 'w') as outfile:
    json.dump(paths_json, outfile)
