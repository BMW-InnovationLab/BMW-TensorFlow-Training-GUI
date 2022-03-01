from abc import ABC, ABCMeta, abstractmethod



class AbstractMemoryContextManager(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def clear_context(self)->None: raise NotImplementedError
