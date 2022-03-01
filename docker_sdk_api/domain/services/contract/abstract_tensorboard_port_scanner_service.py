from typing import Dict
from abc import ABC, abstractmethod
from domain.models.container_info import ContainerInfo
from domain.models.tensorboard_port import TensorboardPort


class AbstractTensorboardPortScannerService(ABC):

    @abstractmethod
    def get_tensorboard_port(self, container_info: ContainerInfo) -> TensorboardPort: raise NotImplementedError

    @abstractmethod
    def get_archived_tensorboard_port(self, container_info: ContainerInfo) -> int: raise NotImplementedError
