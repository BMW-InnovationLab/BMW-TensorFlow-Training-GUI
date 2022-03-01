from abc import ABC, abstractmethod, ABCMeta

from domain.models.container_info import ContainerInfo


class AbstractTensorboardService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def tensorboard_start(self, container_info: ContainerInfo) -> None: raise NotImplementedError

    @abstractmethod
    def tensorboard_stop(self, container_info: ContainerInfo) -> None: raise NotImplementedError

    @abstractmethod
    def tensorboard_delete(self, container_info: ContainerInfo) -> None: raise NotImplementedError
