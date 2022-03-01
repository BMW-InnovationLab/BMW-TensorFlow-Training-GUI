import docker
from domain.exceptions.docker_exception import DockerClientNotInitialized


class DockerClientService():

    def __init__(self):
        self.client = docker.from_env()
