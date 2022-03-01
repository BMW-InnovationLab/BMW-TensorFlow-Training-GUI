from pydantic import BaseModel


class Paths(BaseModel):
    base_dir: str
    api_folder: str
    dataset_folder_on_host: str
    checkpoints_folder_on_host: str
    inference_api_models_folder: str
    image_name: str
    weights_path: str
    checkpoint_path: str
    servable_checkpoints_folder: str
    dataset_folder: str
    networks_path: str
    tensorboards_folder_on_host: str
    tensorboards_path: str
