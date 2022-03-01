from abc import ABC, ABCMeta, abstractmethod

from domain.models.hyper_parameter_information import HyperParameterInformation


class AbstractModelEvaluationService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def evaluate_model(self, hyper_params: HyperParameterInformation)->None: raise NotImplementedError
