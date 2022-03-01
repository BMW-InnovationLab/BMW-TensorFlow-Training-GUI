from application.docker.services.DockerClientService import DockerClientService
from domain.exceptions.dataset_exception import DataNotFound
from domain.exceptions.infrastructure_exception import ContainerNotFound
from domain.models.container_info import ContainerInfo
from domain.models.tensorboard_port import TensorboardPort
from domain.services.contract.abstract_tensorboard_port_scanner_service import AbstractTensorboardPortScannerService
from shared.helpers.alias_provider_sql import get_name_from_alias, get_tensorboard_port_from_name


class TensorboardPortScannerService(AbstractTensorboardPortScannerService):
    def __init__(self, docker_client: DockerClientService):
        self.client: DockerClientService = docker_client.client

    def get_tensorboard_port(self, container_info: ContainerInfo) -> TensorboardPort:
        tensorboard_port: int = None
        api_port: int = None
        try:
            for container in self.client.containers.list():
                if (container.name == get_name_from_alias(container_info.name)):
                    tensorboard_port = int(container.ports['6006/tcp'][0]['HostPort'])
                    api_port = int(container.ports['5252/tcp'][0]['HostPort'])
            return TensorboardPort(tensorboard_port=tensorboard_port, api_port=api_port)
        except Exception:
            raise ContainerNotFound(container_name=container_info.name)

    def get_archived_tensorboard_port(self, container_info: ContainerInfo) -> int:
        try:
            tensorboard_port: int = get_tensorboard_port_from_name(container_info.name)
            print(tensorboard_port)
            return tensorboard_port
        except Exception as e:
            raise DataNotFound(additional_message=e.__str__(), column_name="name", table_name="tensorboardTable")
