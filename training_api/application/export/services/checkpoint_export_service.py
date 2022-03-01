import os
import shutil
from distutils.dir_util import copy_tree

from application.paths.services.path_service import PathService
from domain.exceptions.export_exception import PathNotFound
from domain.models.network_information import NetworkInformation
from domain.models.paths import Paths
from domain.services.contract.abstract_checkpoint_export_service import AbstractCheckpointExportService


class CheckpointExportService(AbstractCheckpointExportService):
    """
     A class used to save checkpoint to checkpoint directory

    ...

     Attributes
    ----------
    path : Paths
        DTO containing all necessary paths

    Methods
    -------
    save_checkpoint( network_info: NetworkInformation) -> None
        save the trained model to checkpoint directory to be used as pre-trained model
    """

    def __init__(self, path: PathService):
        self.path: Paths = path.get_paths()

    def save_checkpoint(self, network_info: NetworkInformation) -> None:
        network_checkpoint: str = os.path.join(self.path.checkpoints_dir, network_info.network_architecture)
        model_checkpoint: str = os.path.join(network_checkpoint, network_info.model_name)
        model_export_dir: str = os.path.join(self.path.export_dir, 'checkpoint')
        try:
            if not os.path.exists(network_checkpoint) and not os.path.isdir(network_checkpoint):
                os.makedirs(network_checkpoint)

            if os.path.exists(model_checkpoint) and os.path.isdir(model_checkpoint):
                shutil.rmtree(model_checkpoint)
            os.makedirs(model_checkpoint)

            # shutil.copy2(model_export_dir, model_checkpoint)
            copy_tree(model_export_dir, model_checkpoint)
        except Exception as e:
            raise PathNotFound(additional_message=e.__str__(), path=model_export_dir)
