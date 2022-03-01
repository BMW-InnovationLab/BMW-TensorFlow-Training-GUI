import json
import urllib.request
import tarfile
import os
import shutil

from distutils.dir_util import copy_tree
from typing import Dict, List

"""
download and store models from TF model zoo

"""


def get_url_weight_dict() -> List[Dict]:
    """
    format
    [
    {
        "name": "resnet50",
        "selected": true,
        "url": "http://test.com/dhjd.tar"
    }
    ]
    """
    weights_lst = []
    select_all: bool = weights_dict['select_all']

    for key, value in weights_dict.items():
        json_obj = {}

        if key != "select_all":
            json_obj["name"] = key
            json_obj["selected"] = value or select_all
            json_obj["url"] = weight_to_url[key]
            weights_lst.append(json_obj)
    return weights_lst


def download_weight(weights_name: str, weight_url: str):
    print("Downloading " + str(weights_name), flush=True)

    urllib.request.urlretrieve(weight_url, "./test.tar.gz")
    tar = tarfile.open("./test.tar.gz", "r:gz")
    tar.extractall()
    tar.close()
    all_subdirs = [d for d in os.listdir('.') if os.path.isdir(d)]
    latest_subdir = min(all_subdirs, key=os.path.getmtime)
    src_path = os.path.join(".", latest_subdir)
    dest_path = os.path.join("/weights", weights_name)
    copy_tree(src_path, dest_path)
    shutil.rmtree(src_path)
    os.remove("./test.tar.gz")


if __name__ == "__main__":
    weights_dict: Dict[str, bool] = json.load(open('assets/networks.json', 'rb'))
    weight_to_url: Dict[str, str] = json.load(open('assets/networks_url.json', 'rb'))
    weights_list = get_url_weight_dict()
    for weight_dict in weights_list:
        if weight_dict["selected"]:
            download_weight(weights_name=weight_dict["name"], weight_url=weight_dict["url"])
