import os
import shutil

from application.paths.services.path_service import PathService
from domain.exceptions.export_exception import PathNotFound
from domain.models.network_information import NetworkInformation
from domain.models.paths import Paths
from domain.services.contract.abstract_servable_export_service import AbstractServableExportService


class ServableExportService(AbstractServableExportService):
    """
     A class used to save model as zip file

    ...

     Attributes
    ----------
    path : Paths
        DTO containing all necessary paths

    Methods
    -------
    save_servable_model(network_info: NetworkInformation) -> None
        create zip file containing the exported model
    """

    def __init__(self, path: PathService):
        self.path: Paths = path.get_paths()

    def _create_servable_dir(self, network_architecture: str) -> None:
        servable_dir: str = os.path.join(self.path.servable_dir, network_architecture)
        if not os.path.exists(servable_dir) and not os.path.isdir(servable_dir):
            os.mkdir(servable_dir)

    def save_servable_model(self, network_info: NetworkInformation) -> None:
        zip_file_name: str = network_info.model_name
        zip_dir: str = os.path.join(self.path.servable_dir, network_info.network_architecture)
        servable_model_name: str = network_info.model_name + '-' + network_info.network_architecture
        servable_model_path: str = os.path.join(self.path.inference_model_dir, servable_model_name)
        
        # create folder by the name of the network to save the zip file inside it
        self._create_servable_dir(network_architecture=network_info.network_architecture)

        zip_file: str = os.path.join(zip_dir, zip_file_name)

        try:
            shutil.make_archive(zip_file, 'zip', root_dir=servable_model_path)
        except Exception as e:
            raise PathNotFound(additional_message=e.__str__(), path=zip_file)
