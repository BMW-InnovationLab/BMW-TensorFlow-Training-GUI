import json
import os
import shutil
from distutils.dir_util import copy_tree
from typing import Dict, Any

from application.paths.services.path_service import PathService
from application.export.models.InferenceConfiguration import InferenceConfiguration
from domain.exceptions.export_exception import PathNotFound
from domain.models.network_information import NetworkInformation
from domain.models.paths import Paths
from domain.services.contract.abstract_inference_model_export_service import AbstractInferenceModelExportService
from shared.helpers.object_classes_from_json import get_labels_from_json_file


class InferenceModelExportService(AbstractInferenceModelExportService):
    """
     A class used to save model for inference

    ...

     Attributes
    ----------
    path : Paths
        DTO containing all necessary paths

    Methods
    -------
    save_inference_model(network_info: NetworkInformation) -> None
        Copy the exported model to inference models folder and create config.json containing model configuration
    """

    def __init__(self, path: PathService):
        self.path: Paths = path.get_paths()

    def _save_json_config(self, inference_model_path: str, network_name: str) -> None:
        architecture: str = network_name.split('-')[0]
        number_of_classes: int = len(get_labels_from_json_file(self.path.object_classes_path))
        config: Dict[str, Any] = InferenceConfiguration(network=architecture,
                                                        number_of_classes=number_of_classes).dict()
        config_json_path: str = os.path.join(inference_model_path, 'config.json')

        with open(config_json_path, 'w') as f:
            json.dump(config, f)


    def save_inference_model(self, network_info: NetworkInformation) -> None:
        inference_model_name: str = network_info.model_name + '-' + network_info.network_architecture
        inference_model_path: str = os.path.join(self.path.inference_model_dir, inference_model_name)
        saved_model_frozen_dir: str = os.path.join(self.path.export_dir, 'saved_model')
        try:
            if os.path.exists(inference_model_path) and os.path.isdir(inference_model_path):
                shutil.rmtree(inference_model_path)
            os.makedirs(inference_model_path)

            shutil.copy2(os.path.join(self.path.training_dir, 'object-detection.pbtxt'), inference_model_path)
            shutil.copy2(os.path.join(self.path.model_dir, 'pipeline.config'), inference_model_path)

            copy_tree(saved_model_frozen_dir, inference_model_path)
            # shutil.copy2(saved_model_frozen_dir, inference_model_path)
        except Exception as e:
            raise PathNotFound(additional_message=e.__str__(), path=saved_model_frozen_dir)
        self._save_json_config(inference_model_path, network_info.network_architecture)
