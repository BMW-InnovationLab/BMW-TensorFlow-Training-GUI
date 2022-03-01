from domain.exceptions.application_error import ApplicationError


class TensorflowInternalError(ApplicationError):
    def __init__(self, additional_message: str = ''):
        super().__init__('Tensorflow Internal Error ', additional_message)