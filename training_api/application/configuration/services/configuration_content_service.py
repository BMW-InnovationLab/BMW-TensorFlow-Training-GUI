import os

from typing import Dict
from object_detection.utils.config_util import get_configs_from_pipeline_file
from application.paths.services.path_service import PathService
from domain.exceptions.configuration_exception import ConfigurationPipelineNotFound
from domain.models.network_information import NetworkInformation
from domain.models.paths import Paths
from domain.services.contract.abstract_configuration_content_service import AbstractConfigurationContentService
from object_detection.utils.config_util import create_pipeline_proto_from_configs, save_pipeline_config


class ConfigurationContentService(AbstractConfigurationContentService):
    def __init__(self, path: PathService):
        self.path: Paths = path.get_paths()

    def _adjust_configuration_content(self, network_path: str, config_file_content: Dict[str, str]) -> Dict[str, str]:

        train_config: Dict[str, str] = config_file_content['train_config']
        train_config.fine_tune_checkpoint = network_path
        train_config.fine_tune_checkpoint_type = "detection"

        train_input_reader: Dict[str, str] = config_file_content['train_input_config']
        train_input_reader.label_map_path = os.path.join(self.path.training_dir, 'object-detection.pbtxt')
        train_input_reader.tf_record_input_reader.input_path[:] = [
            os.path.join(self.path.training_dir, 'train.record')]

        eval_input_reader: Dict[str, str] = config_file_content['eval_input_config']
        eval_input_reader.label_map_path = os.path.join(self.path.training_dir, 'object-detection.pbtxt')
        eval_input_reader.tf_record_input_reader.input_path[:] = [
            os.path.join(self.path.training_dir, 'test.record')]
        return config_file_content

    def get_configuration_content(self, network_info: NetworkInformation) -> str:
        try:
            network_path: str = os.path.join(self.path.weights_dir, network_info.network_architecture,
                                             "pipeline.config")
            config_file_content: Dict[str, str] = get_configs_from_pipeline_file(network_path)
            checkpoint_path = os.path.join(self.path.weights_dir, network_info.network_architecture,
                                           'checkpoint/ckpt-0')
            content: Dict[str, str] = self._adjust_configuration_content(config_file_content=config_file_content,
                                                                         network_path=checkpoint_path)

            # the return of proto dict make error so we save the file and read it with python reader
            pipeline_config = create_pipeline_proto_from_configs(content)
            save_pipeline_config(pipeline_config, "/tmp/")
            content_str: str = open("/tmp/pipeline.config", "r").read()

            return content_str

        except Exception as e:
            raise ConfigurationPipelineNotFound(additional_message=e.__str__(), pipeline_path=network_path)
