
from abc import ABC, abstractmethod
from domain.models.paths import Paths
class AbstractPathService(ABC):
    
    
    @abstractmethod
    def get_paths(self)-> Paths:raise NotImplementedError
   
