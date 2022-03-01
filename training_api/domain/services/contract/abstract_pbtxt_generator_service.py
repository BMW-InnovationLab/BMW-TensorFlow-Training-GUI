from abc import ABC, abstractmethod, ABCMeta


class AbstractPbtxtGenratorService(ABC):

    __metaclass__ = ABCMeta

    @abstractmethod
    def generate_pbtxt(self) -> None: raise NotImplementedError
