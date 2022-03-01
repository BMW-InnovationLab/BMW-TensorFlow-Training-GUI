from pydantic import BaseModel


class InferenceConfiguration(BaseModel):
    """
        A class  used to store config.json fields and default values
    """
    predictions: int = 10
    confidence: int = 60
    inference_engine_name: str = "tensorflow2_detection"
    framework: str = "tensorflow"
    type: str = "detection"
    network: str = None
    number_of_classes: int = None
