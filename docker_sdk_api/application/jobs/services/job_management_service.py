import os
import time
from typing import Dict, List

from application.paths.services.path_service import PathService
from shared.helpers.alias_provider_sql import add_alias, delete_alias, get_name_from_alias, register_tensorboard_mapping
from domain.models.container_settings import ContainerSettings
from domain.services.contract.abstract_job_management_service import AbstractJobManagementService
from domain.models.container_info import ContainerInfo
from shared.helpers.slugified_name_creator import create_slugified_name
from application.docker.services.DockerClientService import DockerClientService
from domain.models.paths import Paths
from domain.exceptions.job_exception import ContainerNotFound
from domain.exceptions.job_exception import JobNotStarted


# noinspection PyCompatibility
class JobManagementService(AbstractJobManagementService):
    def __init__(self, path: PathService, docker_client: DockerClientService):
        self.path: Paths = path.get_paths()
        self.client: DockerClientService = docker_client.client

    def _struct_volumes(self, container_settings: ContainerSettings) -> Dict[str, Dict[str, str]]:
        dataset_path: str = os.path.join(self.path.dataset_folder_on_host, container_settings.dataset_path)
        api_folder: str = self.path.api_folder
        volumes: Dict[str, Dict[str, str]] = {dataset_path: {'bind': '/dataset', 'mode': 'rw'},
            api_folder: {'bind': '/training_api', 'mode': 'rw'},
            self.path.checkpoints_folder_on_host: {'bind': '/checkpoints', 'mode': 'rw'},
            self.path.inference_api_models_folder: {'bind': '/inference_api/models', 'mode': 'rw'},
            self.path.tensorboards_folder_on_host: {'bind': '/tensorboards', 'mode': 'rw'}}
        return volumes

    def _struct_ports(self, container_settings: ContainerSettings) -> Dict[str, str]:
        ports: Dict[str, str] = {'6006/tcp': str(container_settings.tensorboard_port),
                                 '5252/tcp': str(container_settings.api_port)}
        return ports

    def _run_command_cpu(self, ports: Dict[str, str], volumes: Dict):
        return self.client.containers.run(self.path.image_name, remove=True, ports=ports, volumes=volumes, tty=True,
                                          stdin_open=True, detach=True)

    def _run_command_gpu(self, ports: Dict[str, str], volumes: Dict, gpus_string: str):
        return self.client.containers.run(self.path.image_name, remove=True, runtime='nvidia',
                                          environment=[gpus_string], ports=ports, volumes=volumes, tty=True,
                                          stdin_open=True, detach=True)

    def start_container(self, container_settings: ContainerSettings) -> None:

        volumes: Dict[str, Dict[str, str]] = self._struct_volumes(container_settings=container_settings)
        ports: Dict[str, str] = self._struct_ports(container_settings=container_settings)
        string_gpus: List[str] = [str(gpu) for gpu in container_settings.gpus]
        slugified_name: str = create_slugified_name(container_settings.name)

        gpus_string: str = None
        if self.path.image_name.endswith('cpu') and string_gpus[0] == "-1":
            container_name: str = "object_detection_CPU_" + slugified_name
        else:
            gpus_string: str = "NVIDIA_VISIBLE_DEVICES=" + (",".join(string_gpus))
            container_name: str = "object_detection_GPU_" + str("_".join(string_gpus)) + "_" + slugified_name

        try:
            if gpus_string is not None:
                container = self._run_command_gpu(ports=ports, volumes=volumes, gpus_string=gpus_string)
            else:
                container = self._run_command_cpu(ports=ports, volumes=volumes)
            container.rename(container_name)
            add_alias(name=container_name, alias=container_settings.name, model=container_settings.network_architecture,
                      author=container_settings.author, dataset=container_settings.dataset_path)
            register_tensorboard_mapping(container_settings.name, container_settings.tensorboard_port)
            time.sleep(12)
        except Exception as e:
            raise JobNotStarted(additional_message=e.__str__())

    def stop_container(self, container_info: ContainerInfo) -> None:

        for container in self.client.containers.list():
            if container.name == get_name_from_alias(container_info.name):
                container.kill()
                delete_alias(container_info.name)
                return
        raise ContainerNotFound(additional_message="Job Not Killed ", container_name=container_info.name)
