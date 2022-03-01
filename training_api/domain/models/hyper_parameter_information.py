from typing import Optional

from pydantic import BaseModel


class HyperParameterInformation(BaseModel):
    """
        A class  used to store the user requested hyper parameter
    """
    num_classes: int = None
    batch_size: int = None
    learning_rate: float = None
    checkpoint_name: str = None
    width: int = None
    height: int = None
    network_architecture: str
    training_steps: int
    eval_steps: int
    allow_growth : bool 
    name: str
