from pydantic.main import BaseModel


class ConfigurationContent(BaseModel):
    """
        A class  used to store pipeline.config as str
    """
    content: str
