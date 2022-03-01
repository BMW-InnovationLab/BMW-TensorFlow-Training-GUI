from abc import ABC, abstractmethod, ABCMeta

from domain.models.network_information import NetworkInformation


class AbstractConfigurationManager(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def create_config_file(self, network_info: NetworkInformation):raise NotImplementedError
