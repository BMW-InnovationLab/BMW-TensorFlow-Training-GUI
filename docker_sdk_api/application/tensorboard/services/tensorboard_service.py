import os
import shutil
import signal
import subprocess
from typing import List

from application.paths.services.path_service import PathService
from domain.exceptions.tensorboard_exception import *
from domain.models.container_info import ContainerInfo
from domain.models.paths import Paths
from domain.services.contract.abstract_tensorboard_service import AbstractTensorboardService
from shared.helpers.alias_provider_sql import get_tensorboard_port_from_name, delete_tensorboard_mapping


class TensorboardService(AbstractTensorboardService):
    """
     A class used to manage tensorboard
    ...

     Attributes
    ----------
    path : Paths
        DTO containing all necessary paths

    Methods
    -------
    tensorboard_start(container_info: ContainerInfo) -> None
        start tensorboard using subprocess and save pid to file
    tensorboard_stop(container_info: ContainerInfo) -> None
        kill tensorboard process
    tensorboard_delete(container_info: ContainerInfo) -> None
        delete tensorboard directory and mapping from DB

    """

    def __init__(self, path: PathService):
        self.path: Paths = path.get_paths()

    def tensorboard_start(self, container_info: ContainerInfo) -> None:
        port: int = get_tensorboard_port_from_name(container_info.name)
        log_dir: str = os.path.join(self.path.tensorboards_path, container_info.name)
        command: List[str] = ["tensorboard", "--host", "0.0.0.0", "--logdir", log_dir, "--port", str(port)]
        pid_file: str = os.path.join(log_dir, "pid.txt")

        try:
            p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except Exception as e:
            raise TensorboardProcessNotStarted(additional_message=e.__str__())

        with open(pid_file, "w") as f:
            f.write(str(p.pid))
            f.close()

    def tensorboard_stop(self, container_info: ContainerInfo) -> None:
        log_dir: str = os.path.join(self.path.tensorboards_path, container_info.name)
        pid_file: str = os.path.join(log_dir, "pid.txt")
        try:
            if os.path.isfile(pid_file) and os.stat("file").st_size != 0:
                with open(pid_file, "r") as f:
                    pid = f.read()
                    os.kill(int(pid), signal.SIGKILL)
                    f.close()

        except Exception as e:
            open(pid_file, 'w').close()

    def tensorboard_delete(self, container_info: ContainerInfo) -> None:
        log_dir: str = os.path.join(self.path.tensorboards_path, container_info.name)
        try:
            self.tensorboard_stop(container_info)
            shutil.rmtree(log_dir)
            delete_tensorboard_mapping(container_info.name)
        except OSError as e:
            print(e)
            raise TensorboardPathNotFound(additional_message=e.__str__(), tensorboard_path=log_dir)
