import os
import shutil
from distutils.dir_util import copy_tree

from application.paths.services.path_service import PathService
from domain.exceptions.export_exception import PathNotFound
from domain.models.network_information import NetworkInformation
from domain.models.paths import Paths
from domain.services.contract.abstract_tensorboard_export_service import AbstractTensorboardExportService


class TensorboardExportService(AbstractTensorboardExportService):
    """
     A class used to save tensorboard to tensorboard directory

    ...

     Attributes
    ----------
    path : Paths
        DTO containing all necessary paths

    Methods
    -------
    save_tensorboard( network_info: NetworkInformation) -> None
        save the trained model's tensorboard to tensorboard directory to be used when the model training is done
    """

    def __init__(self, path: PathService):
        self.path: Paths = path.get_paths()

    def save_tensorboard(self, network_info: NetworkInformation) -> None:
        model_tensorboard: str = os.path.join(self.path.tensorboards_dir, network_info.model_name)
        model_tensorboard_export_dir: str = self.path.log_dir
        try:
            if os.path.exists(model_tensorboard) and os.path.isdir(model_tensorboard):
                shutil.rmtree(model_tensorboard)

            eval_dir: str = os.path.join(model_tensorboard, "eval")
            train_dir: str = os.path.join(model_tensorboard, "train")
            os.makedirs(eval_dir)
            os.makedirs(train_dir)

            copy_tree(os.path.join(model_tensorboard_export_dir, "eval"), eval_dir)
            copy_tree(os.path.join(model_tensorboard_export_dir, "train"), train_dir)
        except Exception as e:
            raise PathNotFound(additional_message=e.__str__(), path=model_tensorboard_export_dir)
