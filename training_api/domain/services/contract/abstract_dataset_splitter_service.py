from abc import ABC, abstractmethod, ABCMeta

from domain.models.labels_information import LabelsInformation


class AbstractDatasetSplitterService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def split_dataset(self, labels_info: LabelsInformation) -> None: raise NotImplementedError
