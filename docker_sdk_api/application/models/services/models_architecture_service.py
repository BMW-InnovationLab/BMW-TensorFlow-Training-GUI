import os
from typing import List
import json
from application.paths.services.path_service import PathService
from domain.models.paths import Paths
from domain.services.contract.abstract_models_architecture_service import AbstractModelsArchitectureService
from domain.exceptions.models_exception import PathNotFound


class ModelsArchitectureService(AbstractModelsArchitectureService):
    def __init__(self, path: PathService):
        self.path = path.get_paths()

    def get_architecture(self) -> List[str]:
        # return all available models architecture

        try:
            with open(self.path.networks_path, 'r') as paths_file:
                json_path = json.load(paths_file)
                networks: List[str] = []

                if json_path["select_all"]:
                    del json_path["select_all"]
                    networks: List[str] = [key for key in json_path.keys()]
                else:
                    del json_path["select_all"]
                    for key, value in json_path.items():
                        if value:
                            networks.append(key)

            return networks
        except Exception as e:
            raise PathNotFound(additional_message=e.__str__(), path=self.path.networks_path)
