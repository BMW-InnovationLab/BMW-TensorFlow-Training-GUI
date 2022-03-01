from application.data_preparation.models.column_name import ColumnName
from application.paths.services.path_service import PathService
from domain.models.labels_information import LabelsInformation
from domain.models.paths import Paths
from domain.services.contract.abstract_dataset_splitter_service import AbstractDatasetSplitterService
import pandas as pd
import random
import os
from typing import List


class DatasetSplitterService(AbstractDatasetSplitterService):
    """
     A class used to split csv file to train test csv

    ...

     Attributes
    ----------
    path : Paths
        DTO containing all necessary paths
    Methods
    -------
    split_dataset(labels_info: LabelsInformation) -> None
        Split a csv file containing images with corresponding classes to train and test csv files
    """

    def __init__(self, path: PathService):
        self.path: Paths = path.get_paths()

    def split_dataset(self, labels_info: LabelsInformation) -> None:
        df = pd.read_csv(os.path.join(self.path.training_dir, "labels.csv"))

        images: List[str] = os.listdir(self.path.images_dir)
        random.shuffle(images)

        index = (int(round(float(labels_info.split_percentage) * len(images))))
        training_images: List[str] = images[:index]
        testing_images: List[str] = images[index:]

        column_name: List[str] = list([col.value for col in ColumnName])

        train = pd.DataFrame(columns=column_name)
        test = pd.DataFrame(columns=column_name)

        for index, row in df.iterrows():
            if row['filename'] in training_images:
                train = train.append(row)
            elif row['filename'] in testing_images:
                test = test.append(row)
        train.to_csv(os.path.join(self.path.training_dir, 'train.csv'), index=False)
        test.to_csv(os.path.join(self.path.training_dir, 'test.csv'), index=False)
        os.remove(os.path.join(self.path.training_dir, 'labels.csv'))
