
import random
import os
import pandas as pd
from sklearn.model_selection import GroupShuffleSplit
from typing import List

from application.data_preparation.models.column_name import ColumnName
from application.paths.services.path_service import PathService
from domain.models.labels_information import LabelsInformation
from domain.models.paths import Paths
from domain.services.contract.abstract_dataset_splitter_service import AbstractDatasetSplitterService



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

    def split_dataset(self, labels_df: pd.DataFrame, labels_info: LabelsInformation) -> None:
        splitter = GroupShuffleSplit(train_size=labels_info.split_percentage, n_splits=1)
        split = splitter.split(labels_df, groups=labels_df['filename'])
        train_inds, test_inds = next(split)

        train = labels_df.iloc[train_inds]
        test = labels_df.iloc[test_inds]
        
        train.to_csv(os.path.join(self.path.training_dir, 'train.csv'), index=False)
        test.to_csv(os.path.join(self.path.training_dir, 'test.csv'), index=False)