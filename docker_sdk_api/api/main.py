import GPUtil
import docker
import time
import json
import os
import uvicorn

from fastapi import FastAPI, Query, HTTPException, File, Form, BackgroundTasks
from pydantic import BaseModel, Schema
from starlette.requests import Request
from starlette.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles



from checkpoint_validator import validate_checkpionts_folder
from dataset_validator import validate_dataset
from dataset_validator import dataset_label_types
from port_scanner import used_ports


client = docker.from_env()
paths = json.loads(open('./paths.json',"r").read())

paths['network_archs_basedir'] = os.path.join(paths['base_dir'],paths['network_archs_basedir'])
paths['api_folder'] = os.path.join(paths['base_dir'],paths['api_folder'])
paths['dataset_folder_on_host'] = os.path.join(paths['base_dir'],paths['dataset_folder_on_host'])
paths['checkpoints_folder_on_host'] = os.path.join(paths['base_dir'],paths['checkpoints_folder_on_host'])
paths['inference_api_models_folder'] = os.path.join(paths['base_dir'],paths['inference_api_models_folder'])

app = FastAPI(version='2.0', title='Docker SDK API',
              description="API for managing training containers")


app.mount("/models", StaticFiles(directory="/checkpoints/servable"), name="models")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DatasetName(BaseModel):
    dataset_name: str

class DatasetInfo(BaseModel):
    dataset_path: str
    labels_type: str


class ContainerInfo(BaseModel):
    name: str

class ContainerSettings(BaseModel):
    name: str
    network_architecture: str
    dataset_path: str
    gpus: int
    tensorboard_port: int
    api_port: int


class NetworkInfo(BaseModel):
    network_architecture: str


"""
Gets the available gpus.

Returns
-------
list of str
    a list of gpu names wuth less than 25% memory consumption

"""
@app.get('/get_gpu_info')
async def get_gpu_info():
    return GPUtil.getAvailable(order = 'memory', limit = 10, maxLoad = 0.25, maxMemory = 0.25, includeNan=False, excludeID=[], excludeUUID=[])
     

"""
Checks if a dataset is valid

Parameters
----------
datasetInfo: DatasetInfo
             object of type DatasetInfo containing the dataset path and the labels type 

Returns
-------
Boolean
        true if the dataset is valid, false otherwise

"""
@app.post('/dataset_validation')
async def dataset_validation(datasetInfo: DatasetInfo):
    return  validate_dataset(os.path.join('/datasets',datasetInfo.dataset_path), datasetInfo.labels_type)
    

"""
Gets all the running training jobs.

Returns
-------
list of str
    a list of all running training jobs names

"""
@app.get('/get_all_jobs')
async def get_containers():
    containers = []
    for container in client.containers.list():
        if(container.image.attrs['RepoTags'][0] == paths['image_name']+":latest"):
            containers.append(container.name)
    return containers


"""
Gets the tensorboard port for a specific job

Parameters
----------
containerInfo: ContainerInfo
               object of type ContainerInfo containing the container name 

Returns
-------
str
    the port on which tensorboard for that specific container is running

""" 
@app.post('/monitor_job')
async def get_tensorboard_port(containerInfo: ContainerInfo):
    for container in client.containers.list():
        if(container.name == containerInfo.name):
            tensorboard_port = int(container.ports['6006/tcp'][0]['HostPort'])
    return tensorboard_port

"""
Stops a specific job

Parameters
----------
containerInfo: ContainerInfo
               object of type ContainerInfo containing the container name 

Returns
-------
str
    Success Message
""" 
@app.post('/stop_job')
async def stop_container(containerInfo: ContainerInfo):
    for container in client.containers.list():
        if(container.name == containerInfo.name):
            container.kill()

    return "Job Killed"


"""
Get logs for a specific job

Parameters
----------
containerInfo: ContainerInfo
               object of type ContainerInfo containing the container name 

Returns
-------
list of str
    logs of the job
"""
@app.post('/get_logs')
async def get_logs(containerInfo: ContainerInfo):
    
    logs = ""

    for container in client.containers.list():
        if(container.name == containerInfo.name):
            logs = container.logs()
    
    log_list = logs.splitlines()
    response_logs = []

    for log in log_list:
        log = log.decode("utf-8")
        response_logs.append(log)

    return response_logs

"""
Starts a job

Parameters
----------
containerSettings: ContainerSettnigs
                   object of type ContainerSettings containing all the necessary info to start a job
Returns
-------
str
    Success Message
""" 
@app.post('/start_job')
async def start_training_api(containerSettings: ContainerSettings):
    NETWORKS_WEIGHTS_FOLDER = paths['network_archs_basedir']
    API_FOLDER = paths['api_folder']
    volumes={os.path.join(paths['dataset_folder_on_host'], containerSettings.dataset_path): {'bind': '/dataset', 'mode': 'rw'}, API_FOLDER: {'bind': '/api', 'mode': 'rw'}, paths['checkpoints_folder_on_host'] : {'bind': '/checkpoints', 'mode': 'rw'}, paths['inference_api_models_folder']: {'bind': '/inference_models', 'mode':'rw'}}
    ports = {'6006/tcp': str(containerSettings.tensorboard_port), '5252/tcp': str(containerSettings.api_port)}
    gpus_string =  "NVIDIA_VISIBLE_DEVICES="+str(containerSettings.gpus)
    container = client.containers.run(paths['image_name'], remove=True, runtime='nvidia', environment=[gpus_string], name=containerSettings.name ,ports=ports, volumes=volumes, tty=True, stdin_open=True, detach=True) 
    time.sleep(8)
    return "Success"


"""
Get all datasets

Returns
-------
list of str
    datasets
"""

@app.get('/get_datasets')
async def get_datasets():
    return os.listdir('/datasets')

"""
Get all network architectures

Returns
-------
list of str
    network architectures
"""
@app.get('/get_archs')
async def get_architectures():
    return os.listdir('/weights')


"""
Get all the pre-trained weights (or checkpoints) for a specific network architecture

Parameters
----------
networkInfo: NetworkInfo
                   object of type NetworkInfo containing the name of the network architecture

Returns
-------
list of str
    checkpoints
"""
@app.post('/get_checkpoints')
async def get_checkpoints(networkInfo: NetworkInfo):
    checkpoints_list = []
    network_checkpoints_folder = os.path.join('/checkpoints', networkInfo.network_architecture)
    for folder in os.listdir(network_checkpoints_folder):
        if  os.path.isdir(os.path.join(network_checkpoints_folder, folder)) and validate_checkpionts_folder(os.path.join(network_checkpoints_folder, folder)):
            checkpoints_list.append(folder)
    
    return checkpoints_list

"""
Get all models in the static folder called servable

Returns
-------
list of str
    servable models
"""
@app.get('/get_downloadable_models')
async def get_downloadable_models():
    servable_checkpoints_folder = '/checkpoints/servable'
    if not os.path.isdir(servable_checkpoints_folder):
        os.makedirs(servable_checkpoints_folder)
    
    models = os.listdir(servable_checkpoints_folder)
    response = []
    for model in models:
        if model.endswith(".zip"):
            response.append(model.split(".zip")[0])  
    return response


"""
Get all the used ports on the system

Returns
-------
list of str
    used ports
"""
@app.get('/get_used_ports')
async def get_used_ports():
    return (used_ports())


"""
Get all finished jobs by comparing the models that are in the servable folder (done training) with the models currently in progress 

Returns
-------
list of str
    finished jobs names
"""
@app.get('/get_finished_jobs')
async def get_finished_jobs():
    downloadable_models = os.listdir("/checkpoints/servable")

    downloadable_jobs = []
    for model in downloadable_models:
        model_name = model.split("zip")[0]
        model_name = model_name.split("-")
        name_to_append = ""
        for i in range(len(model_name)-1):
            name_to_append += model_name[i]
            name_to_append += '-'
        
        name_to_append = name_to_append[:-1]
        downloadable_jobs.append(name_to_append)
    
    running_containers = []
    for container in client.containers.list():
        if(container.image.attrs['RepoTags'][0] == paths['image_name']+":latest"):
            running_containers.append(container.name)
    
    finished_jobs = list(set(running_containers).intersection(set(downloadable_jobs)))
    return finished_jobs


"""
Get the exisiting labels type for a specific dataset

Parameters
----------
datasetInfo: DatasetName
             object of type DatasetNamr containing the dataset name

Returns
-------
list of str
        labels types for the dataset
"""
@app.post('/get_labels_type')
def get_labels_type(dn: DatasetName):
    return(dataset_label_types(os.path.join('/datasets',dn.dataset_name)))