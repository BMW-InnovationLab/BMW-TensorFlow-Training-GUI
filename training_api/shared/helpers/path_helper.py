import json

from domain.models.paths import Paths


def get_path_configuration() -> Paths:
    with open("./assets/paths.json", 'r') as paths_file:
        json_path = json.load(paths_file)
    paths: Paths = Paths.parse_obj(json_path)
    return paths
