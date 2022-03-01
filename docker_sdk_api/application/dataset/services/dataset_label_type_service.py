import os
from typing import List, Set

from application.paths.services.path_service import PathService
from domain.models.dataset_name import DatasetName
from application.dataset.models.label_extension import LabelExtension
from domain.services.contract.abstract_dataset_labels_type_service import AbstractDatasetLabelsTypeService

from domain.models.paths import Paths


class DatasetLabelTypeService(AbstractDatasetLabelsTypeService):
    def __init__(self, path: PathService):
        self.path: Paths = path.get_paths()

    def get_labels_type(self, dataset_name: DatasetName) -> List[str]:
        # get label type from dataset/labels/ and intersect them with supported labels type from Enum
        dataset_folder: str = os.path.join(self.path.dataset_folder, dataset_name.dataset_name)
        label_types: List[str] = os.listdir(os.path.join(dataset_folder, 'labels'))
        extensions_names: Set[str] = set([ext.value for ext in LabelExtension])
        intersected_types: List[str] = list(extensions_names.intersection(set(label_types)))
        return intersected_types
