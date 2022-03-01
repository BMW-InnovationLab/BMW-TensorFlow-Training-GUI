from abc import ABC, abstractmethod, ABCMeta

from domain.models.hyper_parameter_information import HyperParameterInformation


class AbstractModelTrainerService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def train(self, hyper_params: HyperParameterInformation) -> None: raise NotImplementedError
