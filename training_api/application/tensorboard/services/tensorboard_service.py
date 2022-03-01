import subprocess
import os
import signal
from typing import List

from application.paths.services.path_service import PathService
from domain.models.paths import Paths
from domain.services.contract.abstract_tensorboard_service import AbstractTensorboardService
from domain.exceptions.tensorboard_exception import *


class TensorboardService(AbstractTensorboardService):
    """
     A class used to run tensorboard

    ...

     Attributes
    ----------
    path : Paths
        DTO containing all necessary paths

    Methods
    -------
    tensorboard_start() -> None
        start tensorboard using subprocess and save pid to file
    tensorboard_stop() -> None
        kill tensorboard process


    """

    def __init__(self, path: PathService):
        self.path: Paths = path.get_paths()

    def tensorboard_start(self) -> None:
        command: List[str] = ["tensorboard", "--host", "0.0.0.0", "--logdir", str(self.path.log_dir)]

        try:
            p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except Exception as e:
            raise TensorboardProcessNotStarted(additional_message=e.__str__())

        with open(self.path.pid_file, "w") as f:
            f.write(str(p.pid))
            f.close()

    def tensorboard_stop(self) -> None:
        try:
            if os.path.isfile(self.path.pid_file) and os.stat("file").st_size != 0:
                with open(self.path.pid_file, "r") as f:
                    pid = f.read()
                    os.kill(int(pid), signal.SIGKILL)
                    f.close()

        except Exception as e:
            open(self.path.pid_file, 'w').close()
