import requests

from application.docker.services.DockerClientService import DockerClientService
from application.url.services.url_service import UrlService
from domain.exceptions.api_request_exception import ApiRequestException
from domain.exceptions.infrastructure_exception import ContainerNotFound
from domain.models.container_info import ContainerInfo
from domain.models.urls import Urls
from domain.services.contract.abstract_training_api_consumer_service import AbstractTrainingApiConsumerService
from shared.helpers.alias_provider_sql import get_name_from_alias


class TrainingApiConsumerService(AbstractTrainingApiConsumerService):
    """
         A class used to consume the API in training_api

        ...

        Methods
        -------
        refresh_training_api_tensorboard(container_info: ContainerInfo) -> None
            refresh tensorboard in corresponding training_api container

        """

    def __init__(self, docker_client: DockerClientService, url: UrlService):
        self.client: DockerClientService = docker_client.client
        self.url: Urls = url.get_urls()

    def refresh_training_api_tensorboard(self, container_info: ContainerInfo) -> None:
        api_port: int = None
        try:
            for container in self.client.containers.list():
                if container.name == get_name_from_alias(container_info.name):
                    api_port = int(container.ports['5252/tcp'][0]['HostPort'])

            refresh_url = self.url.base_url + str(api_port) + self.url.training_ip_tensorboard_refresh
            response = requests.get(refresh_url)
        except requests.exceptions.RequestException as e:
            print(e)
            raise ApiRequestException(additional_message=e.__str__(), container_name=container_info.name)
        except Exception as e:
            raise ContainerNotFound(additional_message=e.__str__(), container_name=container_info.name)
