from abc import ABC, abstractmethod, ABCMeta

from application.data_preparation.models.tf_record_path import TfRecordPath


class AbstractTfRecordGeneratorService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def generate_tf_record(self, tf_record_path: TfRecordPath) -> None: raise NotImplementedError
