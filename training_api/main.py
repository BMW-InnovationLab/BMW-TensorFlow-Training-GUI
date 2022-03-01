import os
import sys

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from shared.helpers.directories_creator import create_required_directories
from api.controllers import tensorboard_controller, data_preparation_controller, training_controller, \
    configuration_controller


# sys.path.append("/tensorflow/models/research")
create_required_directories()
# todo add the number of worker in the api
os.environ["TF_CPP_MIN_LOG_LEVEL"]="0"
app = FastAPI(version='2.0', title='Tensorflow Object Detection Training API v2',
              description="API for training object detection models using Tensorflow object detection API v2")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    data_preparation_controller.router,
    prefix="/data_preparation",
    tags=["data_preparation"],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    configuration_controller.router,
    prefix="/configuration",
    tags=["configuration"],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    training_controller.router,
    prefix="/training",
    tags=["training"],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    tensorboard_controller.router,
    prefix="/tensorboard",
    tags=["tensorboard"],
    responses={404: {"description": "Not found"}},
)


