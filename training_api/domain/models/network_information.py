from pydantic.main import BaseModel


class NetworkInformation(BaseModel):
    """
        A class  used to store network architecture and model name
    """
    network_architecture: str
    model_name: str = None
