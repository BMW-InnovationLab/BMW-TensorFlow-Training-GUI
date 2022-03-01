import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from api.controllers import jobs_controller, infrastructure_controller, dataset_controller, models_controller, \
    tensorboard_controller

app = FastAPI(version='2.0', title='Docker SDK API',
              description="API for managing training containers")
app.mount("/models_services", StaticFiles(directory="/checkpoints/servable"), name="models_services")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    jobs_controller.router,
    prefix="/jobs",
    tags=["jobs"],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    infrastructure_controller.router,
    prefix="/infrastructure",
    tags=["infrastructure"],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    dataset_controller.router,
    prefix="/dataset",
    tags=["dataset"],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    models_controller.router,
    prefix="/models",
    tags=["models"],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    tensorboard_controller.router,
    prefix="/tensorboard",
    tags=["tensorboard"],
    responses={404: {"description": "Not found"}},
)
