from abc import ABCMeta, abstractmethod, ABC

from domain.models.network_information import NetworkInformation


class AbstractTensorboardExportService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def save_tensorboard(self, network_info: NetworkInformation) -> None: raise NotImplementedError
