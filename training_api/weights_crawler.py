import urllib.request
import tarfile
import os
import shutil

from distutils.dir_util import copy_tree


url_to_folder = {}

URL_SSD_MOBILENET = "http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v1_coco_2018_01_28.tar.gz"
URL_SSD_FPN = "http://download.tensorflow.org/models/object_detection/ssd_resnet50_v1_fpn_shared_box_predictor_640x640_coco14_sync_2018_07_03.tar.gz"
URL_SSD_INCEPTION ="http://download.tensorflow.org/models/object_detection/ssd_inception_v2_coco_2018_01_28.tar.gz"
URL_FRCNN_RESNET_50 = "http://download.tensorflow.org/models/object_detection/faster_rcnn_resnet50_coco_2018_01_28.tar.gz"
URL_FRCNN_RESNET_101 = "http://download.tensorflow.org/models/object_detection/faster_rcnn_resnet101_coco_2018_01_28.tar.gz"



url_to_folder[URL_SSD_MOBILENET] = "ssd_mobilenet"
url_to_folder[URL_SSD_FPN] = "ssd_fpn"
url_to_folder[URL_SSD_INCEPTION] = "ssd_inception"
url_to_folder[URL_FRCNN_RESNET_50] = "frcnn_resnet_50"
url_to_folder[URL_FRCNN_RESNET_101] = "frcnn_resnet_101"


for key, value in url_to_folder.items():

    print("Downloading "+str(value))    
    urllib.request.urlretrieve(key, "./test.tar.gz")
    
    tar = tarfile.open("./test.tar.gz", "r:gz")

    tar.extractall()
    tar.close()
    all_subdirs = [d for d in os.listdir('.') if os.path.isdir(d)]
    latest_subdir = min(all_subdirs, key=os.path.getmtime)
    
    src_path = os.path.join(".", latest_subdir)
    dest_path = os.path.join("/weights", value)
    copy_tree(src_path, dest_path)

    shutil.rmtree(src_path)
    os.remove("./test.tar.gz")



