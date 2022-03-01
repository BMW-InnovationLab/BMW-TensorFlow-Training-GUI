import os
import glob
import pandas as pd
import json
import io

from PIL import Image
from typing import List, Dict, Any

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


def json_to_csv(labels_path, images_path, column_name):
    images: List[str] = os.listdir(images_path)
    labels: List[str] = os.listdir(labels_path)
    json_list: List[Dict[str, str]] = []

    for json_file in labels:
        prefix_name: str = json_file.split('.')[0]

        json_data: Dict[str, str] = json.load(open(os.path.join(labels_path, json_file), "rb"))

        image_name: str = ""
        width: int = 0
        height: int = 0

        for image in images:
            if image.split('.')[0] == prefix_name:
                image_name = image
                width, height = Image.open(os.path.join(images_path, image)).size
                break

        if json_data is not []:

            for obj in json_data:
                value: Dict[str, Any] = {
                    'filename': str(image_name),
                    'width': int(width),
                    'height': int(height),
                    'class': str(obj['ObjectClassName']),
                    'xmin': float(obj['Left']),
                    'ymin': float(obj['Top']),
                    'xmax': float(obj['Right']),
                    'ymax': float(obj['Bottom'])
                }

                json_list.append(value)

    json_df = pd.DataFrame(json_list, columns=column_name)
    return json_df
