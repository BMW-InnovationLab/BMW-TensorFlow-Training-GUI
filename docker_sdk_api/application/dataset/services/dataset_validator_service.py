from application.paths.services.path_service import PathService
from domain.services.contract.abstract_dataset_validator_service import AbstractDatasetValidatorService
import os
from domain.models.dataset_info import DatasetInfo
from domain.exceptions.dataset_exception import DatasetNotValid
from application.dataset.models.label_extension import LabelExtension
from application.dataset.models.image_extension import ImageExtension
from typing import List, Dict
from domain.models.paths import Paths


class DatasetValidatorService(AbstractDatasetValidatorService):
    def __init__(self, path: PathService):
        self.path = path.get_paths()

    def _check_image_format(self, dataset_folder: str) -> bool:
        images: List[str] = os.listdir(os.path.join(dataset_folder, 'images/'))
        # list images and compare them with supported types
        for image in images:
            if image.lower().split('.')[1] not in list(ImageExtension.__members__):
                return False
        return True

    def _check_labels_format(self, dataset_folder: str, labels_type: str) -> bool:
        labels: List[str] = os.listdir(os.path.join(dataset_folder, 'labels/', labels_type))
        # list labels and compare with supported types
        for label in labels:
            if label.lower().split('.')[1] != LabelExtension(labels_type).name:
                return False
        return True

    def validate_dataset(self, dataset_info: DatasetInfo) -> None:

        # validate dataset folder structure
        dataset_folder: str = os.path.join(self.path.dataset_folder, dataset_info.dataset_path)
        if os.path.isdir(os.path.join(dataset_folder, 'images')) and os.path.isdir(
                os.path.join(dataset_folder, 'labels/', dataset_info.labels_type)) and os.path.isfile(
            os.path.join(dataset_folder, 'objectclasses.json')):
            # check folder contents
            if self._check_image_format(dataset_folder=dataset_folder) and self._check_labels_format(
                    dataset_folder=dataset_folder,
                    labels_type=dataset_info.labels_type):
                return
        raise DatasetNotValid(dataset_name=dataset_info.dataset_path)
