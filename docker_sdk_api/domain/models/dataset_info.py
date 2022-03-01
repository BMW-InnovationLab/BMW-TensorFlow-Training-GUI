from pydantic import BaseModel

class DatasetInfo(BaseModel):
    dataset_path: str
    labels_type: str
