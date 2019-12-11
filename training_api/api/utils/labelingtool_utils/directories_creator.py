import os
import shutil


"""
 creates required directories
"""
def create_required_directories():
    if os.path.isdir('/training_dir'):
         shutil.rmtree('/training_dir') 

    os.makedirs('/training_dir/data')
    os.makedirs('/training_dir/model')