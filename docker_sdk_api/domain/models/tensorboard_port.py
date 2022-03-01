from pydantic import BaseModel


class TensorboardPort(BaseModel):
    tensorboard_port: int
    api_port: int
