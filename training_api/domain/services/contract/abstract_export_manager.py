from abc import ABC, abstractmethod, ABCMeta

from domain.models.network_information import NetworkInformation


class AbstractExportManager(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def save_trained_model(self,network_info: NetworkInformation) -> None: raise NotImplementedError
