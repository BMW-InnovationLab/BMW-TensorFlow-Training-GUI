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

            json_data = json.load(open(path+'/'+json_file,"rb"))

            image_name = ""
            width = 0
            height = 0


            for image in images:
                if image.startswith(prefix_name):
                    image_found = True
                    image_name = image
                    width, height = Image.open(images_path+'/'+image).size
                    break
                

            if image_found == True and json_data is not []:

                for obj in json_data:

                    value = {}

                    value['filename'] = str(image_name)
                    value['width'] = int(width)
                    value['height'] = int(height)

                    value['class'] = str(obj['ObjectClassName'])
                    value['xmin'] = float(obj['Left'])
                    value['ymin'] = float(obj['Top'])
                    value['xmax'] = float(obj['Right'])
                    value['ymax'] = float(obj['Bottom'])
                    

                    json_list.append(value)
        
                
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    json_df = pd.DataFrame(json_list, columns=column_name)
    return json_df
