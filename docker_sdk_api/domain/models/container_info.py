from typing import Optional

from pydantic import BaseModel


class ContainerInfo(BaseModel):
    name: str
    model: Optional[str]
    dataset: Optional[str]
    author: Optional[str]
