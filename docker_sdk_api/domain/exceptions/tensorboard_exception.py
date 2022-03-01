from domain.exceptions.application_error import ApplicationError


class TensorboardProcessInvalid(ApplicationError):
    def __init__(self, additional_message: str = ''):
        super().__init__('Tensorboard Process Could Not Be Killed ', additional_message)


class TensorboardProcessNotStarted(ApplicationError):
    def __init__(self, additional_message: str = ''):
        super().__init__('Tensorboard Process Could Not Be Started ', additional_message)


class TensorboardPathNotFound(ApplicationError):
    def __init__(self, additional_message: str = '', tensorboard_path: str = ''):
        super().__init__('Tensorboard Path Not Found ', additional_message + ' {}'.format(tensorboard_path))
