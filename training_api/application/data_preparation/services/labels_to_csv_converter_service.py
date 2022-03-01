import os

from typing import List, Dict

from application.data_preparation.converter.json_converter import JsonConverter
from application.data_preparation.converter.pascal_converter import PascalConverter
from application.data_preparation.models.converter_configuration_enum import ConverterConfigurationEnum
from application.paths.services.path_service import PathService
from domain.models.labels_information import LabelsInformation
from domain.models.paths import Paths
from domain.services.contract.abstract_converter_service import AbstractConverterService
from domain.services.contract.abstract_labels_to_csv_converter_service import AbstractLabelsToCsvConverterService


class LabelsToCsvConverterService(AbstractLabelsToCsvConverterService):
    """
     A class used to split dataset to train test data

    ...

     Attributes
    ----------
    path : Paths
        DTO containing all necessary paths
    Methods
    -------
    convert_to_csv(labels_info: LabelsInformation) -> None
        convert json and xml labels to a csv files containing images and classes with bounding box information using
        converter object with factory design patter and ConverterConfigurationEnum to get supporter extension
    """

    def __init__(self, path: PathService):
        self.path: Paths = path.get_paths()
        self.converter_instances: Dict[str, AbstractConverterService] = {}
        self.converter_mappings: Dict[str, AbstractConverterService] = {}
        self._initialize_mappings_()

    def _initialize_mappings_(self) -> None:
        self.network_mappings = {
            ConverterConfigurationEnum.json.value: JsonConverter,
            ConverterConfigurationEnum.xml.value: PascalConverter,
        }

    # factory design pattern
    def convert_to_csv(self, labels_info: LabelsInformation) -> AbstractConverterService:
        format_name: str = labels_info.labels_type.lower()
        if format_name in self.converter_instances:
            return self.converter_mappings.get(format_name.lower())

        else:
            converter: AbstractConverterService = self.network_mappings.get(format_name)(self.path)
            self.converter_instances[format_name] = converter
            return converter.convert_to_csv()

