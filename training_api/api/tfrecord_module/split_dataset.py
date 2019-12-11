import pandas as pd
import numpy as np
import os

"""
splits a csv  dataset file into training and testing

Parameters
----------
input_path: str
            path of label file

split_percentage: float
            percentage to assign for training and testing
    
"""

def split_dataset(input_path, split_percentage):
    df = pd.read_csv(input_path)

    msk = np.random.rand(len(df)) <= float(split_percentage)

    train = df[msk]
    test = df[~msk]

    train.to_csv('/training_dir/data/train.csv', index=False)
    test.to_csv('/training_dir/data/test.csv', index=False)
    os.remove(input_path)