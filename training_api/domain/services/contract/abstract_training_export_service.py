from abc import ABCMeta, ABC, abstractmethod

from domain.models.network_information import NetworkInformation


class AbstractTrainingWriterService(ABC):
    __metaclass__ = ABCMeta

    def save_training_model(self, network_info: NetworkInformation) -> None: raise NotImplementedError
