import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import json
import io
import csv

from PIL import Image
from utils.labelingtool_utils.json_to_csv import json_to_csv
from utils.labelingtool_utils.xml_to_csv import xml_to_csv


"""
calls xml_to_csv and json_to_csv to generate a labels pandas dataframe 
then dumps the dataframe to a csv file

Parameters
----------
images_path: str
            path of the images folder

labels_path: str
            path of the labels folder

output_path: str
            path of the folder to store the resulting csv file

labels_type: str
            type of labels

"""


def labels_to_csv(images_path, labels_path, output_path, labels_type):
    labels_df = None

    if labels_type == "json":
        labels_df = json_to_csv(labels_path, images_path)
        labels_df.to_csv(output_path, index=None)

    elif labels_type == "pascal":
        column_name, xml_list = xml_to_csv(labels_path)
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=column_name)
            writer.writeheader()
            for row in xml_list:
                writer.writerow(row)


     
    print('Successfully converted xml to csv.')






