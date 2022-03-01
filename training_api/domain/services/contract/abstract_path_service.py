from abc import abstractmethod, ABC, ABCMeta

from domain.models.paths import Paths


class AbstractPathService(ABC):

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_paths(self) -> Paths: raise NotImplementedError
