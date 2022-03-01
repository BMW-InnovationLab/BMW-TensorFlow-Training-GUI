from domain.exceptions.application_error import ApplicationError


class ApiRequestException(ApplicationError):
    def __init__(self, additional_message: str = '', container_name: str = ''):
        super().__init__('Api Request failed for container {}: '.format(container_name), additional_message)