from application.docker.services.DockerClientService import DockerClientService
from application.tensorboard.services.tensorboard_service import TensorboardService
from application.consumers.services.training_api_consumer_service import TrainingApiConsumerService
from domain.models.container_info import ContainerInfo
from domain.services.contract.abstract_tensorboard_refresh_service import AbstractTensorboardRefreshService
from shared.helpers.alias_provider_sql import get_name_from_alias


class TensorboardRefreshService(AbstractTensorboardRefreshService):
    """
     A class used to refresh host or training_api tensorboard

    ...

    Methods
    -------
    tensorboard_refresh(container_info: ContainerInfo) -> None
        refreshes tensorboard host or training_api tensorboard depending on container's availability

    """

    def __init__(self, docker_client: DockerClientService,
                 training_api_tensorboard_service: TrainingApiConsumerService,
                 tensorboard_service: TensorboardService):
        self.client: DockerClientService = docker_client.client
        self.training_api_tensorboard_service: TrainingApiConsumerService = training_api_tensorboard_service
        self.tensorboard_service: TensorboardService = tensorboard_service

    def tensorboard_refresh(self, container_info: ContainerInfo) -> None:
        if get_name_from_alias(container_info.name) in map(lambda container: container.name,
                                                           self.client.containers.list()):
            self.training_api_tensorboard_service.refresh_training_api_tensorboard(container_info)
        else:
            self.tensorboard_service.tensorboard_stop(container_info)
            self.tensorboard_service.tensorboard_start(container_info)
