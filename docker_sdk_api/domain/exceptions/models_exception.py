from domain.exceptions.application_error import ApplicationError


class PathNotFound(ApplicationError):
    def __init__(self, additional_message: str = '', path: str = ''):
        super().__init__("Path Not Found  ", additional_message + '{}'.format(path))
