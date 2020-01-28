import json
import sys
import os
import shutil

from zipfile import ZipFile

from utils.framework_utils.training import train
from utils.framework_utils.export_inference_graph import export_graph
from utils.labelingtool_utils.object_classes_handler import get_labels_from_json_file

"""
Train and export a model

Parameters
----------
training_steps: int
               number of training steps

evaluation_steps: int
               number of evaluation steps

model_name: str
                given name of the model

network_arch: str
                name of the network architecture

"""
def train_and_export(training_steps, evaluation_steps, model_name, network_arch):
    train(None, '/training_dir/model', '/training_dir/model/pipeline.config', training_steps, evaluation_steps, network_arch)
   
    trained_checkpoint_prefix = '/training_dir/model/model.ckpt-'+str(training_steps)
    export_graph(None, '/training_dir/model/pipeline.config', trained_checkpoint_prefix, '/training_dir/model')
    

    MODEL_EXPORT_BASEPATH = '/export'
    model_export_destination = os.path.join(MODEL_EXPORT_BASEPATH, model_name)


    if not os.path.isdir(MODEL_EXPORT_BASEPATH):
        os.makedirs(MODEL_EXPORT_BASEPATH)

    if os.path.exists(model_export_destination) and os.path.isdir(model_export_destination):
        shutil.rmtree(model_export_destination)
    
    os.makedirs(model_export_destination)


    CHECKPOINTS_BASEPATH = '/checkpoints'
    arch_checkpoints_folder = os.path.join(CHECKPOINTS_BASEPATH, network_arch)
    model_checkpoints_folder = os.path.join(arch_checkpoints_folder, model_name)
    servable_checkpoints_folder = os.path.join(CHECKPOINTS_BASEPATH, 'servable')

    if not os.path.isdir(arch_checkpoints_folder):
        os.makedirs(arch_checkpoints_folder)

    if os.path.exists(model_checkpoints_folder) and os.path.isdir(model_checkpoints_folder):
        shutil.rmtree(model_checkpoints_folder)

    os.makedirs(model_checkpoints_folder)


    if not os.path.isdir(servable_checkpoints_folder):
        os.makedirs(servable_checkpoints_folder)

    shutil.copy2('/training_dir/model/frozen_inference_graph.pb', model_export_destination)
    shutil.copy2('/training_dir/model/pipeline.config', model_export_destination)
    shutil.copy2('/training_dir/data/object-detection.pbtxt', model_export_destination)
    

    labels = get_labels_from_json_file("/dataset/objectclasses.json")
    
    if (network_arch.startswith('ssd')):
        architecture = 'ssd'
    else:
        architecture = 'fasterrcnn'
    
    config = {"predictions":15, "confidence":10, "inference_engine_name": "tensorflow_detection", "framework": "tensorflow", "type": "detection", "network": architecture, "number_of_classes": len(labels)} 
    config_json_path = os.path.join(model_export_destination, 'config.json')
    
    with open(config_json_path, 'w') as f: 
        json.dump(config, f)


    for f in os.listdir('/training_dir/model'):
        if f.startswith('model.ckpt-'+str(training_steps)):
            shutil.copy2('/training_dir/model/'+f, model_checkpoints_folder)

    # zip_file_name = model_name + '.zip'
    zip_file_name = model_name+'-'+network_arch+'.zip'
    zip_file = os.path.join(servable_checkpoints_folder, zip_file_name)

    inference_model_path = os.path.join('/inference_models', model_name) 
    # os.makedirs(inference_model_path)
    shutil.copytree(model_export_destination, inference_model_path)

    with ZipFile(zip_file, 'w') as zipObj:
       for filename in os.listdir(model_export_destination):
               filePath = os.path.join(model_export_destination, filename)
               zipObj.write(filePath)


