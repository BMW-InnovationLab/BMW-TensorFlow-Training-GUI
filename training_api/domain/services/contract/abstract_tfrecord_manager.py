from abc import ABC, abstractmethod, ABCMeta

from domain.models.labels_information import LabelsInformation


class AbstractDataPreparationManager(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def prepare_dataset(self, labels_info: LabelsInformation) -> None: raise NotImplementedError
