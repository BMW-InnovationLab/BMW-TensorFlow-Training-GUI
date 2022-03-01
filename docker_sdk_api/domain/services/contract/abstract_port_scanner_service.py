from typing import List
from abc import ABC, abstractmethod


class AbstractPortScannerService(ABC):

    @abstractmethod
    def get_used_ports(self) -> List[str]: raise NotImplementedError
