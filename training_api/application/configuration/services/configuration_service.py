import json
import os

from typing import Dict
from application.configuration.models.network_configuration_enum import NetworkConfigurationEnum
from object_detection.utils.config_util import get_configs_from_pipeline_file
from application.paths.services.path_service import PathService
from domain.exceptions.configuration_exception import ConfigurationPipelineNotFound
from domain.models.network_information import NetworkInformation
from domain.models.paths import Paths
from domain.services.contract.abstract_configuration_service import AbstractConfigurationService
from shared.helpers.object_classes_from_json import get_labels_from_json_file
from domain.exceptions.configuration_exception import DefaultConfigurationFileNotFound


class ConfigurationService(AbstractConfigurationService):
    """
     A class used to return configuration

    ...

     Attributes
    ----------
    network_instances : Dict[str, AbstractConfigureNetworkService]
        dict containing created instance of class AbstractConfigureNetworkService
    network_mappings :Dict[str, AbstractConfigureNetworkService]
        dict used to map between configuration network name and configuration class template

    Methods
    -------
    get_configurations( network_info: NetworkInformation) -> str
        take a network name and return str the pipeline.config corresponding to that network name

    get_config_file_content( network_info: NetworkInformation) -> Dict[str, str]:
        take network name and return dict containing the configs using TF internal function
    get_default_configuration(network_info: NetworkInformation) -> Dict
        take network name and return the default configuration (batch, num_classes etc.)
        from the default_config.json file
    """

    def __init__(self, path: PathService):
        self.path: Paths = path.get_paths()

    def _get_network_learning_rate_base(self,network_architecture:str)-> float :
        network_path: str = os.path.join(self.path.weights_dir,network_architecture,"pipeline.config")
        content :Dict[str, str] = get_configs_from_pipeline_file(network_path)
        return round(content['train_config'].optimizer.momentum_optimizer.learning_rate.cosine_decay_learning_rate.learning_rate_base, 5)


    def get_configurations(self, network_info: NetworkInformation) -> str:
        try:
            network_path: str = os.path.join(self.path.weights_dir, network_info.network_architecture,
                                             "pipeline.config")
            content: str = open(network_path, "r").read()
            return content
        except Exception as e:
            raise ConfigurationPipelineNotFound(additional_message=e.__str__(), pipeline_path=network_path)

    def get_config_file_content(self, network_info: NetworkInformation) -> Dict[str, str]:
        try:
            network_path: str = os.path.join(self.path.weights_dir, network_info.network_architecture,
                                             "pipeline.config")
            return get_configs_from_pipeline_file(network_path)
        except Exception as e:
            raise ConfigurationPipelineNotFound(additional_message=e.__str__(), pipeline_path=network_path)

    def get_default_configuration(self, network_info: NetworkInformation) -> Dict:
        try:
            with open(self.path.default_configuration_file, 'r') as default_configs:
                json_default_configs = json.load(default_configs)

            num_classes = len(get_labels_from_json_file(self.path.object_classes_path))
            json_default_configs['num_classes'] = num_classes
            json_default_configs['learning_rate']= self._get_network_learning_rate_base(network_architecture = network_info.network_architecture)
            if network_info.network_architecture not in [NetworkConfigurationEnum.SSD_RESNET50_V1_FPN_640x640.value, NetworkConfigurationEnum.SSD_MOBILENET_V1_FPN_640x640.value] :
                del json_default_configs['width']
                del json_default_configs['height']
            return json_default_configs
        except Exception as e:
            raise DefaultConfigurationFileNotFound(additional_message=e.__str__(),
                                                   default_configuration_file=self.path.default_configuration_file)
