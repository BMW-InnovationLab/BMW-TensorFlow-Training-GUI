from abc import ABC, abstractmethod
from typing import List
from domain.models.dataset_name import DatasetName


class AbstractDatasetLabelsTypeService(ABC):

    @abstractmethod
    def get_labels_type(self, dataset_name: DatasetName)-> List[str]: raise NotImplementedError
