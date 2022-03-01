from abc import ABC, abstractmethod, ABCMeta

from typing import Dict

class AbstractConfigurationExportService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def write_configuration(self, configuration_pipeline: Dict[str,str]) -> None: raise NotImplementedError
