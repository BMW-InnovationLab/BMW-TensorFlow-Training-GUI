from pydantic import BaseModel
from typing import List


class ContainerSettings(BaseModel):
    name: str
    network_architecture: str
    dataset_path: str
    gpus: List[int]
    tensorboard_port: int
    api_port: int
    author: str
