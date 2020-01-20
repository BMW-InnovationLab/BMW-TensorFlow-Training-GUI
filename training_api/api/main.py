import sys
import json
import ast

from fastapi import FastAPI, Query, HTTPException, File, Form, BackgroundTasks
from pydantic import BaseModel, Schema 
from starlette.requests import Request
from starlette.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware

from pbtxt_module.pbtxt_generator import generate_pbtxt
from tfrecord_module.more_labels_than_images import delete_images_with_no_labels
from tfrecord_module.labels_to_csv import labels_to_csv
from tfrecord_module.split_dataset import split_dataset
from tfrecord_module.generate_tfrecord import convert_to_tf_record
from config_file_module.create_config_file import create_config_file
from utils.framework_utils.start_tensorboard import start_tensorboard
from utils.labelingtool_utils.directories_creator import create_required_directories
from utils.framework_utils.background_train_export import train_and_export
from utils.labelingtool_utils.object_classes_handler import get_labels_from_json_file

sys.path.append("/tensorflow/models/research")
from object_detection.utils import config_util


create_required_directories() 
start_tensorboard()

app = FastAPI(version='2.0', title='Tensorflow Object Detection Training API',
              description="API for training object detection models using Tensorflow")



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LabelsInfo(BaseModel):
    labels_type: str
    split_percentage: float


class HyperParamsInfo(BaseModel):
    num_classes: int
    batch_size: int
    learning_rate: float 
    checkpoint_path : str = None
    width: int = None
    height: int = None
    network_architecture: str
    training_steps: int
    eval_steps: int
    name: str


class AdvancedConfig(BaseModel):
    content: str
    training_steps: int
    eval_steps: int
    network_architecture: str
    name: str


class DefaultHyperParams(BaseModel):
    network_architecture: str

"""
Creates the pbtxt file

Returns
-------
str
    Success Message
""" 
@app.get('/create_pbtxt')
async def generate_pbtxt_endpoint():
    generate_pbtxt()
    return "Success"

"""
Starts a job

Parameters
----------
labelsInfo: LabelsInfo
                object of type LabbelInfo containing the labels_type and the train test split ratio
            
Returns
-------
str
    Success Message
""" 
@app.post('/create_tfrecord')
async def create_tfrecord_endpoint(labelsInfo: LabelsInfo):
    
    IMAGES_PATH = '/dataset/images'
    LABELS_PATH = '/dataset/labels/'+labelsInfo.labels_type
    LABELS_CSV_PATH = '/training_dir/data/labels.csv'

    delete_images_with_no_labels(IMAGES_PATH, LABELS_PATH)
    labels_to_csv(IMAGES_PATH, LABELS_PATH, LABELS_CSV_PATH,  labelsInfo.labels_type)
    split_dataset(IMAGES_PATH, LABELS_CSV_PATH, labelsInfo.split_percentage)
    convert_to_tf_record(None, '/training_dir/data/train.csv', '/training_dir/data/train.record', IMAGES_PATH)
    convert_to_tf_record(None, '/training_dir/data/test.csv', '/training_dir/data/test.record', IMAGES_PATH)
    return "Success"

"""
Adjusts the training config file and starts the training in the background 

Parameters
----------
hpInfo: HyperParamsInfo
                object of type HyperParamsInfo containing the hyperparameters for the training
            
Returns
-------
str
    Success Message
""" 
@app.post('/config')
async def create_config_endpoint(hpInfo: HyperParamsInfo, background_tasks: BackgroundTasks):
    config_params = hpInfo.dict()
    print(config_params)
    create_config_file('/weights/'+hpInfo.network_architecture+'/configuration.config', config_params, hpInfo.network_architecture)

    background_tasks.add_task(train_and_export, hpInfo.training_steps, hpInfo.eval_steps, hpInfo.name, hpInfo.network_architecture)

    return "Job Started"


"""
Gets the content of the config file for a specific network 

Parameters
----------
dhp: DefaultHyperParams
        object of type DefaultHyperParams containing the netowrk architecture
            
Returns
-------
str
    config file content
""" 
@app.post('/get_config_content')
async def get_config_content(dhp: DefaultHyperParams):
    content = open('/weights/'+dhp.network_architecture+'/configuration.config',"r").read()
    return {"content": content}


"""
Gets a config file from the user and starts the training in the background 

Parameters
----------
advConfig: AdvancedConfig
                object of type AdvancedConfig containing the hyperparameters for the training
            
Returns
-------
str
    Success Message
""" 
@app.post('/config_advanced')
async def create_config_advanced(advConfig: AdvancedConfig, background_tasks: BackgroundTasks):
    open("/training_dir/model/pipeline.config","w").write(advConfig.content)
    background_tasks.add_task(train_and_export, advConfig.training_steps, advConfig.eval_steps, advConfig.name, advConfig.network_architecture)
    return "Job Started"



"""
Gets a set of default hyperparameters for a specific network architecture 

Parameters
----------
dhp: DefaultHyperParams
        object of type DefaultHyperParams containing the netowrk architecture
            
Returns
-------
str
    config file content
""" 
@app.post('/get_default_hyperparameters')
async def get_default_hyperparameters(dhp: DefaultHyperParams):
    labels = get_labels_from_json_file('/dataset/objectclasses.json')
    default_params = {
        "num_classes": len(labels),
        "batch_size": 1,
        "learning_rate": 0.001, 
        "training_steps": 1000,
        "eval_steps": 40    
    }

    if dhp.network_architecture == "ssd_mobilenet" or dhp.network_architecture == "ssd_inception":
        default_params["width"] = 300
        default_params["height"] = 300

    elif dhp.network_architecture == "ssd_resnet_50" or dhp.network_architecture == "ssd_fpn":
        default_params["width"] = 640
        default_params["height"] = 640
    
    return default_params