from abc import ABC, abstractmethod, ABCMeta


class AbstractTensorboardService(ABC):

    __metaclass__ = ABCMeta

    @abstractmethod
    def tensorboard_start(self) -> None: raise NotImplementedError

    @abstractmethod
    def tensorboard_stop(self) -> None: raise NotImplementedError
