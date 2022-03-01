from pydantic import BaseModel


class Paths(BaseModel):
    """
        A class  used to store all necessary paths
    """
    log_dir: str
    pid_file: str
    images_dir: str
    labels_dir: str
    training_dir: str
    object_classes_path: str
    label_map_path: str
    model_dir: str
    weights_dir: str
    export_dir: str
    checkpoints_dir: str
    servable_dir: str
    inference_model_dir: str
    default_configuration_file: str
    tensorboards_dir: str