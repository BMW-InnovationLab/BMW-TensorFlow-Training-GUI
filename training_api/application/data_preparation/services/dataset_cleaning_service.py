import os
from typing import List, Set

from application.paths.services.path_service import PathService
from domain.models.paths import Paths
from domain.models.labels_information import LabelsInformation
from domain.services.contract.abstract_dataset_cleaning_service import AbstractDatasetCleaningService
from application.data_preparation.models.labels_extension_enum import LabelsExtensionEnum


class DatasetCleaningService(AbstractDatasetCleaningService):
    """
     A class used to represent an dataset cleaning

    ...

     Attributes
    ----------
    path : Paths
        DTO containing all necessary paths
    Methods
    -------
    clean_dataset(labels_info: LabelsInformation) -> None
        Makes sure that all images have labels and delete labels with no images

    """

    def __init__(self, path: PathService):
        self.path: Paths = path.get_paths()

    # delete images with no labels
    def clean_dataset(self, labels_info: LabelsInformation) -> None:
        labels_path: str = os.path.join(self.path.labels_dir, str(labels_info.labels_type))
        images: List[str] = [image.split(".")[0] for image in os.listdir(self.path.images_dir)]
        labels: List[str] = [label.split(".")[0] for label in os.listdir(labels_path)]

        intersection: Set[str] = set(labels).intersection(images)

        labels_with_no_images: Set[str] = set(labels) - intersection

        [os.remove(
            os.path.join(labels_path, str(label + "." + LabelsExtensionEnum(labels_info.labels_type).name))) for label
            in
            labels_with_no_images]
