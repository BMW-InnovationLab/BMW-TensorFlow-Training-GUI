import docker


class DockerClient():
    _instance = None

    @staticmethod
    def get_instance():
        if DockerClient._instance == None:
            DockerClient()
        return DockerClient._instance

    def __init__(self):
        self.client = docker.from_env()
        if DockerClient._instance is None:
            DockerClient._instance = self
        else:
            raise Exception(" Error creating another Singleton instance ")

    # def get_dockerClient(self):
    #     return docker.from_env()

