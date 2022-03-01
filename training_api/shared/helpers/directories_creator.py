import os
import shutil

"""
 creates required directories
"""


def create_required_directories() -> None:
    if os.path.isdir('/assets/training_dir'):
        shutil.rmtree('/assets/training_dir')

    os.makedirs('/assets/training_dir/data')
    os.makedirs('/assets/training_dir/model')
# todo change path to root
