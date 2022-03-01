from typing import Dict
from abc import ABC, abstractmethod


class AbstractGpuService(ABC):
    @abstractmethod
    def get_gpu_info(self) -> Dict[str, str]: raise NotImplementedError
