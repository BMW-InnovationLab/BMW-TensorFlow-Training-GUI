from typing import List
from abc import ABC, abstractmethod


class AbstractDatasetService(ABC):

    @abstractmethod
    def get_datasets(self) -> List[str]: raise NotImplementedError
