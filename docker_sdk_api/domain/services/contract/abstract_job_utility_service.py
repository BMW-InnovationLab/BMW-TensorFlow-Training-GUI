from abc import ABC, abstractmethod
from domain.models.paths import Paths
from typing import List
from domain.models.container_info import ContainerInfo


class AbstractJobUtilityService(ABC):
    @abstractmethod
    def get_all_jobs(self) -> List[str]: raise NotImplementedError

    @abstractmethod
    def get_finished_jobs(self) -> List[str]: raise NotImplementedError

    @abstractmethod
    def get_container_logs(self, container_info: ContainerInfo) -> List[str]: raise NotImplementedError
