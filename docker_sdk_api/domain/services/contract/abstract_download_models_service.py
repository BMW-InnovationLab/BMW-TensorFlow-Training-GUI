from typing import Dict
from abc import ABC, abstractmethod


class AbstractDownloadModelsService(ABC):

    @abstractmethod
    def get_downloadable_models(self) -> Dict[str,str]: raise NotImplementedError