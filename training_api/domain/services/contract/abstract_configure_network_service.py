from abc import ABC, abstractmethod, ABCMeta

from typing import Dict

from application.paths.services.path_service import PathService
from domain.models import hyper_parameter_information


class AbstractConfigureNetworkService(ABC):
    __metaclass__ = ABCMeta


    @abstractmethod
    def config_network(self, config_file_content: Dict[str, str], config_params: hyper_parameter_information) -> Dict[
        str, str]: raise NotImplementedError
