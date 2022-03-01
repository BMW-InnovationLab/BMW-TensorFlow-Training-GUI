import codecs
import os
from typing import Dict

from application.paths.services.path_service import PathService
from domain.models.configuration_content import ConfigurationContent
from domain.models.paths import Paths
from domain.services.contract.abstract_configuration_export_service import AbstractConfigurationExportService
from object_detection.utils.config_util import create_pipeline_proto_from_configs, save_pipeline_config
from domain.exceptions.export_exception import *


class ConfigurationExportService(AbstractConfigurationExportService):
    """
     A class used to write pipeline.config file

    ...

     Attributes
    ----------
    path : Paths
        DTO containing all necessary paths

    Methods
    -------
    write_configuration(configuration_pipeline: Dict[str, str]) -> None
        takes a dict containing configuration and create a pipeline proto to be saved as pipeline.config

    write_advanced_configuration(configuration_content: ConfigurationContent) -> None
        takes a str containing configuration and  saved it inside pipeline.config
    """

    def __init__(self, path: PathService):
        self.path: Paths = path.get_paths()

    def write_configuration(self, configuration_pipeline: Dict[str, str]) -> None:
        try:
            pipeline_config = create_pipeline_proto_from_configs(configuration_pipeline)
        except Exception as e:
            raise ConfigurationBodyCorrupter(additional_message=e.__str__())
        try:
            save_pipeline_config(pipeline_config, self.path.model_dir)
        except Exception:
            raise ModelTrainingPathNotFound(training_model_path=self.path.model_dir)

    def write_advanced_configuration(self, configuration_content: ConfigurationContent) -> None:
        try:
            contents: str = codecs.decode(configuration_content.content, "unicode_escape")
            pipeline_config_path: str = os.path.join(self.path.model_dir, 'pipeline.config')
            open(pipeline_config_path, "w").write(contents)
        except Exception as e:
            raise PipelineConfigurationFileNotCreated(additional_message=e.__str__(),
                                                      pipeline_conifg_path=pipeline_config_path)
