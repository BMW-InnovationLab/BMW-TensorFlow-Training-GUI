from application.paths.services.path_service import PathService
from domain.services.contract.abstract_dataset_service import AbstractDatasetService
from typing import List
import os
from domain.models.paths import Paths
from domain.exceptions.dataset_exception import DatasetPathNotFound


class DatasetService(AbstractDatasetService):
    def __init__(self, path: PathService):
        self.path: Paths = path.get_paths()

    def get_datasets(self) -> List[str]:
        try:
            return os.listdir(self.path.dataset_folder)
        except Exception as e:
            raise DatasetPathNotFound(e.__str__())
