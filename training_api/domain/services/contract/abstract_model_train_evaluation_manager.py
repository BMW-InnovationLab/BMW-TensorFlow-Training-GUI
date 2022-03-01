from abc import ABC, abstractmethod, ABCMeta

from domain.models.hyper_parameter_information import HyperParameterInformation


class AbstarctModelTrainEvaluationManager(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def train_eval_continuously(self, hyper_params: HyperParameterInformation) -> None: raise NotImplementedError
