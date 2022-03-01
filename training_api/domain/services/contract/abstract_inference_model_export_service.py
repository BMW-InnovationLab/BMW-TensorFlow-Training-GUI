from abc import ABCMeta, abstractmethod, ABC

from domain.models.network_information import NetworkInformation


class AbstractInferenceModelExportService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def save_inference_model(self, network_info: NetworkInformation) -> None: raise NotImplementedError
