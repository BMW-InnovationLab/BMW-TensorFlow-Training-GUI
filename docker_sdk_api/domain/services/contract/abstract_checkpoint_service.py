from abc import ABC, abstractmethod
from domain.models.network_info import NetworkInfo
from typing import List


class AbstractCheckpointService(ABC):

    def get_checkpoint(self, network_info: NetworkInfo) -> List[str]:raise NotImplementedError
