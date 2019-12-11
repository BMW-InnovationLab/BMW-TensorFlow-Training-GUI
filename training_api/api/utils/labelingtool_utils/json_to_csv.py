import os
import glob
import pandas as pd
import json
import io

from PIL import Image


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


def json_to_csv(path, images_path):    
    images = os.listdir(images_path)
    labels = os.listdir(path)
    json_list = []

    for json_file in labels:
        if (json_file.endswith('.json')):
            # to prevent labels not having images
            image_found = False
            prefix_name = json_file.split('.')[0]
            # json_data = json.loads(io.open(path+'/'+json_file,"r", encoding='utf-8').read())
            json_data = json.load(open(path+'/'+json_file,"rb"))            

            image_name = ""
            width = 0
            height = 0

            value = {}

            for image in images:
                if image.startswith(prefix_name):
                    image_found = True
                    image_name = image
                    width, height = Image.open(images_path+'/'+image).size
                    break
                
            value['filename'] = str(image_name)
            value['width'] = int(width)
            value['height'] = int(height)
            
            if image_found == True and json_data is not []:
                for i in range(len(json_data)):
                    class_name = str(json_data[i]['ObjectClassName'])
                    xmin = float(json_data[i]['Left'])
                    ymin = float(json_data[i]['Top'])
                    xmax = float(json_data[i]['Right'])
                    ymax = float(json_data[i]['Bottom'])


                    value['class'] = class_name
                    value['xmin'] = xmin
                    value['ymin'] = ymin
                    value['xmax'] = xmax
                    value['ymax'] = ymax
                    
                    # value = (
                        # str(image_name),
                        # int(width),
                        # int(height),
                        # class_name,
                        # xmin,
                        # ymin,
                        # xmax,
                        # ymax
                    # )

            json_list.append(value)
    
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    json_df = pd.DataFrame(json_list, columns=column_name)
    return json_df
