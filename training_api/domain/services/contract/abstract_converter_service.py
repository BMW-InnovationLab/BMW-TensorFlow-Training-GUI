from abc import ABC, abstractmethod, ABCMeta

from domain.models.paths import Paths


class AbstractConverterService(ABC):
    __metaclass__ = ABCMeta

    def __init__(self, path: Paths):
        self.path: Paths = path

    @abstractmethod
    def convert_to_csv(self) -> None: raise NotImplementedError
