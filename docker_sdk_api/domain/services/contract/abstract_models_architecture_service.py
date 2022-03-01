from typing import List
from abc import ABC, abstractmethod


class AbstractModelsArchitectureService(ABC):

    @abstractmethod
    def get_architecture(self) -> List[str]: raise NotImplementedError
