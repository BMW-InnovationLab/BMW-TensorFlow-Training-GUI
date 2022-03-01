import json
import os

from application.data_preparation.models.tf_record_path import TfRecordPath
from application.data_preparation.services.dataset_splitter_service import DatasetSplitterService
from application.data_preparation.services.labels_to_csv_converter_service import LabelsToCsvConverterService
from application.data_preparation.services.pbtxt_generator_service import PbtxtGeneratorService
from application.data_preparation.services.tfrecords_generator_service import TfRecordGeneratorService
from application.paths.services.path_service import PathService
from domain.exceptions.application_error import ApplicationError
from domain.models.labels_information import LabelsInformation
from domain.models.paths import Paths
from domain.services.contract.abstract_tfrecord_manager import AbstractDataPreparationManager
from application.data_preparation.services.dataset_cleaning_service import DatasetCleaningService


class DataPreparationManager(AbstractDataPreparationManager):
    """
     A class used to create tf records

    ...

    Methods
    -------
    create_tf_record(labels_info: LabelsInformation) -> None
        Facade design to create tf record by cleaning dataset then converting it to csv file and splitting it
        and then generating tf records
    """

    def __init__(self, path: PathService, dataset_cleaning: DatasetCleaningService,
                 dataset_splitter: DatasetSplitterService,
                 labels_to_csv_converter: LabelsToCsvConverterService, pbtxt_generator: PbtxtGeneratorService,
                 tfrecords_generator: TfRecordGeneratorService):
        self.path: Paths = path.get_paths()
        self.dataset_cleaning = dataset_cleaning
        self.dataset_splitter = dataset_splitter
        self.labels_to_csv_converter = labels_to_csv_converter
        self.pbtxt_generator = pbtxt_generator
        self.tfrecords_generator = tfrecords_generator

    def _create_csv_files(self, labels_info: LabelsInformation) -> None:
        self.dataset_cleaning.clean_dataset(labels_info=labels_info)
        self.labels_to_csv_converter.convert_to_csv(labels_info=labels_info)
        self.dataset_splitter.split_dataset(labels_info=labels_info)

    def _create_tf_record(self):
        # create tf records for train and test
        input_path: str = os.path.join(self.path.training_dir, 'train.csv')
        output_path: str = os.path.join(self.path.training_dir, 'train.record')
        self.tfrecords_generator.generate_tf_record(
            tf_record_path=TfRecordPath(input_path=input_path, output_path=output_path))
        input_path: str = os.path.join(self.path.training_dir, 'test.csv')
        output_path: str = os.path.join(self.path.training_dir, 'test.record')
        self.tfrecords_generator.generate_tf_record(
            tf_record_path=TfRecordPath(input_path=input_path, output_path=output_path))

    def prepare_dataset(self, labels_info: LabelsInformation) -> None:
        try:
            self._create_csv_files(labels_info=labels_info)
            self.pbtxt_generator.generate_pbtxt()
            self._create_tf_record()
        except Exception as e:
            raise ApplicationError(default_message=e.__str__())
