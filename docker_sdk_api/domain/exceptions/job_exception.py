from domain.exceptions.application_error import ApplicationError


class ContainerNotFound(ApplicationError):
    def __init__(self, additional_message: str = '', container_name: str = ''):
        super().__init__("Container Name Not Found ", additional_message + '{}'.format(container_name))


class JobNotStarted(ApplicationError):
    def __init__(self, additional_message: str = '', container_name: str = ''):
        super().__init__("Job Not Started ", additional_message + '{}'.format(container_name))


class ListIndexOutOfRange(ApplicationError):
    def __init__(self, additional_message: str = '', container_id: str = ''):
        super().__init__("The running container has no RepoTag please kill to proceed  ",
                         additional_message + '{}'.format(container_id))
