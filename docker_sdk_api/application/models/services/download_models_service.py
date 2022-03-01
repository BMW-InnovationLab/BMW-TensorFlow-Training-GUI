import os
from typing import List, Dict

from application.paths.services.path_service import PathService
from domain.services.contract.abstract_download_models_service import AbstractDownloadModelsService
from domain.models.paths import Paths

from domain.exceptions.models_exception import PathNotFound

from shared.helpers.get_model_zip import  get_downloadable_zip 
class DownloadModelsService(AbstractDownloadModelsService):

    def __init__(self, path: PathService):
        self.path = path.get_paths()

    def get_downloadable_models(self) -> Dict[str, str]:

        servable_checkpoints_folder: str = self.path.servable_checkpoints_folder
        if not os.path.isdir(servable_checkpoints_folder):
            os.makedirs(servable_checkpoints_folder)

        # response: List[str] = []
        # try:
        #
        #     for model in os.listdir(servable_checkpoints_folder):
        #         if model.endswith(".zip"):
        #             response.append(model.split(".zip")[0])
        #     return response
        # except Exception:
        #     raise PathNotFound(path=servable_checkpoints_folder)
        try:
            response : Dict[str,str]= get_downloadable_zip(folder_path =servable_checkpoints_folder )
            return response
        except Exception:
            raise PathNotFound(path=servable_checkpoints_folder)
