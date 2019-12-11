import sys
import os
sys.path.append("/tensorflow/models/research")

from object_detection.utils import config_util
from config_file_module.ssd_resnet_50_fpn import config_ssd_resnet_fpn
from config_file_module.ssd_mobilenet_inception import config_ssd_mobilenet_inception
from config_file_module.frcnn_resnet_50_101 import config_frcnn_resnet_50_101

"""
modifies the config file of an architecture based on user input 

Params
------

input_path: str
            path of the original config file

config_params: dict
            dict containing all user defined params


network_type: str
            type of the network.


"""
def create_config_file(input_path, config_params, network_type):
    configs = config_util.get_configs_from_pipeline_file(input_path)

    if config_params['checkpoint_path'] is not None:
        prefix = ""
        for ckpt_file in os.listdir(os.path.join('/checkpoints/'+ network_type, config_params['checkpoint_path'])):
            if ckpt_file.endswith(".index"):
                prefix = ckpt_file.split(".index")[0]
                config_params['checkpoint_path'] = '/checkpoints/'+network_type+'/'+config_params['checkpoint_path']+'/'+prefix


    else:
        config_params['checkpoint_path'] = '/weights/'+network_type+'/model.ckpt'

    new_configs = None

    if network_type == "ssd_mobilenet" or network_type == "ssd_inception":
        new_configs = config_ssd_mobilenet_inception(configs, config_params)

    elif network_type == "ssd_resnet_50" or network_type == "ssd_fpn":
        new_configs = config_ssd_mobilenet_inception(configs, config_params)

    elif network_type == "frcnn_resnet_50" or network_type == "frcnn_resnet_101":
        new_configs = config_frcnn_resnet_50_101(configs, config_params)
        

    pipeline_config = config_util.create_pipeline_proto_from_configs(new_configs)
    
    config_util.save_pipeline_config(pipeline_config, '/training_dir/model')

    