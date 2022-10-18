import os
from typing import List
import pandas as pd
from application.data_preparation.models.column_name import ColumnName
from domain.models.paths import Paths
from domain.services.contract.abstract_converter_service import AbstractConverterService
from shared.helpers.xml_to_csv_converter import xml_to_csv


class PascalConverter(AbstractConverterService):
    def __init__(self, path: Paths):
        super().__init__(path=path)

    def convert_to_csv(self) -> pd.DataFrame:
        column_name: List[str] = list([col.value for col in ColumnName])
        # output_path: str = os.path.join(self.path.training_dir, 'labels.csv')
        labels_path: str = os.path.join(self.path.labels_dir, "pascal")

        labels_df = xml_to_csv(labels_path=labels_path, column_name=column_name)
        # labels_df.to_csv(output_path, index=None)
        return labels_df
