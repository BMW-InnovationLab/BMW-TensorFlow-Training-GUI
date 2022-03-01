from abc import ABC, abstractmethod, ABCMeta

from domain.models.labels_information import LabelsInformation


class AbstractDatasetCleaningService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def clean_dataset(self, labels_info: LabelsInformation) -> None: raise NotImplementedError
