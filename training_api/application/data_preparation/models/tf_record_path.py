from pydantic.main import BaseModel


class TfRecordPath(BaseModel):
    """
        A class  used to store the input and output folders where tf record and csv will be stored
    """
    input_path: str
    output_path: str
