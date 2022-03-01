from abc import ABC, abstractmethod
from domain.models.dataset_info import DatasetInfo
from domain.models.api_response import ApiResponse

class AbstractDatasetValidatorService(ABC):

    @abstractmethod
    def validate_dataset(self, dataset_info: DatasetInfo) -> None: raise NotImplementedError
