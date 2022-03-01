from pydantic.main import BaseModel


class LabelsInformation(BaseModel):
    """
        A class  used to store labels type and splitting ration for train/test
    """
    labels_type: str
    split_percentage: float
