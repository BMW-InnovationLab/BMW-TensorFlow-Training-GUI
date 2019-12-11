import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import json
import io
import csv


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

def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        objects = root.findall('object')

        if len(objects) == 0:
            value = {
                "filename": root.find('filename').text,
                "width": int(root.find('size')[0].text),
                "height": int(root.find('size')[1].text),
            }
            xml_list.append(value) 

        else:
            for member in objects:
                value = {
                         "filename": root.find('filename').text,
                         "width": int(root.find('size').find('width').text),
                         "height": int(root.find('size').find('height').text),
                         "class": str(member.find('name').text),
                         "xmin": float(member.find('bndbox').find('xmin').text),
                         "ymin": float(member.find('bndbox').find('ymin').text),
                         "xmax": float(member.find('bndbox').find('xmax').text),
                         "ymax": float(member.find('bndbox').find('ymax').text)
                        #  "xmin": float(member[4][0].text),
                        #  "ymin": float(member[4][1].text),
                        #  "xmax": float(member[4][2].text),
                        #  "ymax": float(member[4][3].text)
                         
                        }   
                xml_list.append(value)
                
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    return column_name, xml_list
