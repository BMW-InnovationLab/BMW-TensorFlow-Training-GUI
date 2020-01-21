import pandas as pd
import numpy as np
import os
import random

"""
splits a csv  dataset file into training and testing

Parameters
----------
input_path: str
            path of label file

split_percentage: float
            percentage to assign for training and testing
    
"""

def split_dataset(images_path, input_path, split_percentage):
    df = pd.read_csv(input_path)

    
    images = os.listdir(images_path)
    random.shuffle(images)

    index = (int(round(float(split_percentage) * len(images))))
    training_images = images[:index]
    testing_images = images[index:]

    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    train = pd.DataFrame(columns=column_name)
    test = pd.DataFrame(columns=column_name)

    for index, row in df.iterrows():
        
        if(row['filename'] in training_images):
            train = train.append(row)
        elif (row['filename'] in testing_images):
            test = test.append(row)
    
    
    
    train.to_csv('/training_dir/data/train.csv', index=False)
    test.to_csv('/training_dir/data/test.csv', index=False)

    os.remove(input_path)