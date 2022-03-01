from abc import ABC, abstractmethod, ABCMeta


class AbstractExportInferenceGraphService(ABC):

    __metaclass__ = ABCMeta

    @abstractmethod
    def export_model(self) -> None: raise NotImplementedError
