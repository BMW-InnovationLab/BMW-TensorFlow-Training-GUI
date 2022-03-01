from pydantic import BaseModel


class Urls(BaseModel):
    """
        A class used to store all necessary urls
    """
    base_url: str
    training_ip_tensorboard_refresh: str
