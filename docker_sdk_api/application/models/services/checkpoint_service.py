from application.paths.services.path_service import PathService
from domain.services.contract.abstract_checkpoint_service import AbstractCheckpointService
from domain.models.paths import Paths
import os
from domain.models.network_info import NetworkInfo
from typing import List
from domain.exceptions.models_exception import PathNotFound


class CheckpointService(AbstractCheckpointService):
    def __init__(self, path: PathService):
        self.path = path.get_paths()

    def _validate_checkpoint(self, network_checkpoints_folder: str) -> bool:
        valid: bool = False

        checkpoint_txt: str = None
        index_file: str = None
        meta_file: str = None

        for ckpt_file in os.listdir(network_checkpoints_folder):
            if ckpt_file == ("checkpoint"):
                checkpoint_txt = ckpt_file
            elif ckpt_file.startswith("ckpt-") and ckpt_file.endswith(".index"):
                index_file = ckpt_file
            elif ckpt_file.startswith("ckpt-") and ckpt_file.endswith(".data-00000-of-00001"):
                meta_file = ckpt_file

        if meta_file is not None and index_file is not None and checkpoint_txt is not None:
            valid = True

        return valid

    def get_checkpoint(self, network_info: NetworkInfo) -> List[str]:
        checkpoints_list: List[str] = []
        network_checkpoints_folder: str = os.path.join(self.path.checkpoint_path, network_info.network_architecture)
        try:
            if os.path.isdir(network_checkpoints_folder):
                for folder in os.listdir(network_checkpoints_folder):
                    if os.path.isdir(os.path.join(network_checkpoints_folder, folder)) and self._validate_checkpoint(
                            os.path.join(network_checkpoints_folder, folder)) and os.path.exists(
                        network_checkpoints_folder):

                        checkpoints_list.append(folder)

            return checkpoints_list
        except Exception:
            raise PathNotFound(path=network_checkpoints_folder)
