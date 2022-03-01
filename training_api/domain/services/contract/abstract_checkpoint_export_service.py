from abc import ABCMeta, abstractmethod, ABC

from domain.models.network_information import NetworkInformation


class AbstractCheckpointExportService(ABC):
    __metaclass__ = ABCMeta


    @abstractmethod
    def save_checkpoint(self, network_info: NetworkInformation) -> None: raise NotImplementedError
