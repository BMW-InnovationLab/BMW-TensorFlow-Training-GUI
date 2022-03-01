from abc import ABC, abstractmethod, ABCMeta

from typing import Dict

from domain.models.network_information import NetworkInformation


class AbstractConfigurationContentService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_configuration_content(self, network_info: NetworkInformation) -> str: raise NotImplementedError
