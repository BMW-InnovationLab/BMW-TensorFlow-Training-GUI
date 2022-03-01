from abc import ABC, abstractmethod, ABCMeta

from domain.models.labels_information import LabelsInformation


class AbstractLabelsToCsvConverterService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def convert_to_csv(self, labels_info: LabelsInformation) -> None: raise NotImplementedError
