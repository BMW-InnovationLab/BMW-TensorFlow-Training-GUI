from domain.exceptions.application_error import ApplicationError


class DockerClientNotInitialized(ApplicationError):
    def __init__(self, additional_message: str = ''):
        super().__init__('Error Creating Another Singleton Instance ', additional_message)
