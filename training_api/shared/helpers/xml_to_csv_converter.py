import glob
import xml.etree.ElementTree as ET
from typing import List, Dict, Any
import random
import pandas as pd

"""
converts a folder containing pascal labels to a pandas dataframe

Parameters
----------
path: str
      labels path



Returns
-------
Pandas Dataframe
            Dataframe containing the labels.

"""


def xml_to_csv(labels_path: str, column_name: List[str]) -> pd.DataFrame:
    xml_list: List[Dict[str, str]] = []
    xml_files_list = glob.glob(labels_path + '/*.xml')
    random.shuffle(xml_files_list)

    for xml_file in xml_files_list:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        objects = root.findall('object')

        if len(objects) == 0:
            value: Dict[str, Any] = {
                "filename": root.find('filename').text,
                "width": int(root.find('size')[0].text),
                "height": int(root.find('size')[1].text),
            }
            xml_list.append(value)

        else:
            for member in objects:
                value: Dict[str, Any] = {
                    "filename": root.find('filename').text,
                    "width": int(root.find('size').find('width').text),
                    "height": int(root.find('size').find('height').text),
                    "class": str(member.find('name').text),
                    "xmin": float(member.find('bndbox').find('xmin').text),
                    "ymin": float(member.find('bndbox').find('ymin').text),
                    "xmax": float(member.find('bndbox').find('xmax').text),
                    "ymax": float(member.find('bndbox').find('ymax').text)

                }
                xml_list.append(value)
    xml_df = pd.DataFrame(data=xml_list, columns=column_name)
    return xml_df