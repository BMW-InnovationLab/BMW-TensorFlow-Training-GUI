from domain.exceptions.application_error import ApplicationError


class GpuInfoInvalid(ApplicationError):
    def __init__(self, additional_message: str = ''):
        super().__init__("Gpu Info Invalid", additional_message)


class ContainerNotFound(ApplicationError):
    def __init__(self, additional_message: str = '', container_name: str = ''):
        super().__init__("Container Name Not Found ", additional_message + '{}'.format(container_name))
