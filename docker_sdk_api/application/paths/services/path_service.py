import json
import os

from domain.models.paths import Paths
from domain.services.contract.abstract_path_service import AbstractPathService


class PathService(AbstractPathService):
    def __init__(self):
        with open("./assets/paths.json", 'r') as paths_file:
            json_path = json.load(paths_file)

            json_path["api_folder"] = os.path.join(json_path["base_dir"], json_path["api_folder"])
            json_path["dataset_folder_on_host"] = os.path.join(json_path["base_dir"],
                                                               json_path["dataset_folder_on_host"])
            json_path["checkpoints_folder_on_host"] = os.path.join(json_path["base_dir"],
                                                                   json_path["checkpoints_folder_on_host"])
            json_path["inference_api_models_folder"] = os.path.join(json_path["base_dir"],
                                                                    json_path["inference_api_models_folder"])
            # json_path["weights_path"]= os.path.join(json_path["base_dir"],
            #                                         json_path["weights_path"])
            json_path["tensorboards_folder_on_host"] = os.path.join(json_path["base_dir"],
                                                                    json_path["tensorboards_folder_on_host"])
            json_path["tensorboards_path"] = os.path.join(json_path["base_dir"], json_path["tensorboards_path"])

            self.paths: Paths = Paths.parse_obj(json_path)

    def get_paths(self) -> Paths:
        return self.paths
