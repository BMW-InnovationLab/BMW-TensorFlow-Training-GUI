import json
import os
from typing import List, Dict
import random
import pandas as pd
from pymage_size import get_image_size

"""
converts a folder containing json labels to a pandas dataframe

Parameters
----------
path: str
      labels path

images_path: str
      images path


Returns
-------
Pandas Dataframe
            Dataframe containing the labels.

"""


def json_to_csv(labels_path, images_path, column_name) -> pd.DataFrame:
    json_list: List[Dict] = []

    images = os.listdir(images_path)
    random.shuffle(images)
    for image_filename in images:
        with open(os.path.join(labels_path, image_filename.rsplit(".", 1)[0] + ".json"), "rb") as f:
            json_data = json.load(f)

        width, height = get_image_size(os.path.join(images_path, image_filename)).get_dimensions()
        json_list.extend([
            {
                'filename': image_filename,
                'width': width,
                'height': height,
                'class': str(obj['ObjectClassName']),
                'xmin': int(obj['Left']),
                'ymin': int(obj['Top']),
                'xmax': int(obj['Right']),
                'ymax': int(obj['Bottom'])
            } for obj in json_data
        ])
    json_df = pd.DataFrame(json_list, columns=column_name)
    return json_df
