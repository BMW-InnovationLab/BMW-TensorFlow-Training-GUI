from abc import ABC, abstractmethod
from domain.models.container_settings import ContainerSettings
from domain.models.container_info import ContainerInfo


class AbstractJobManagementService(ABC):

    @abstractmethod
    def start_container(self, container_settings: ContainerSettings) -> None: raise NotImplementedError

    @abstractmethod
    def stop_container(self, container_info: ContainerInfo) -> None: raise NotImplementedError
