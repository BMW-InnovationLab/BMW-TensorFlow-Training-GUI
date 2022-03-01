from abc import ABC, abstractmethod, ABCMeta

from domain.models.container_info import ContainerInfo


class AbstractTensorboardRefreshService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def tensorboard_refresh(self, container_info: ContainerInfo) -> None: raise NotImplementedError
