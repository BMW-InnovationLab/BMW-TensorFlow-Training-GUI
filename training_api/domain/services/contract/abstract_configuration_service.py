from abc import ABC, abstractmethod, ABCMeta
from domain.models.network_information import NetworkInformation


class AbstractConfigurationService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_configurations(self, network_inf: NetworkInformation) -> str: raise NotImplementedError
