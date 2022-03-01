import json

from domain.models.paths import Paths
from domain.services.contract.abstract_path_service import AbstractPathService


class PathService(AbstractPathService):
    """
     A class used to get paths from path.json and return object of type Paths

    ...

    """

    def __init__(self):
        with open("./assets/paths.json", 'r') as paths_file:
            json_path = json.load(paths_file)
            self.paths: Paths = Paths.parse_obj(json_path)

    def get_paths(self) -> Paths:
        return self.paths
