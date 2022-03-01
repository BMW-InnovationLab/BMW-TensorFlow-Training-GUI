from abc import ABC, ABCMeta, abstractmethod

from domain.models.network_information import NetworkInformation


class AbstractServableExportService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def save_servable_model(self, network_info: NetworkInformation) -> None: raise NotImplementedError
