from domain.exceptions.application_error import ApplicationError


class DatasetPathNotFound(ApplicationError):
    """Raised when the dataset structure is not valid """

    def __init__(self, additional_message: str = '', dataset_path: str = ''):
        super().__init__('Dataset Path Not Found ', additional_message + ' {}'.format(dataset_path))


class DatasetNotValid(ApplicationError):
    def __init__(self, additional_message: str = '', dataset_name: str = ''):
        super().__init__('Dataset Not Valid ', additional_message + ' {}'.format(dataset_name))


class DataNotFound(ApplicationError):
    def __init__(self, additional_message: str = '', column_name: str = '', table_name: str = ''):
        super().__init__('{} '.format(column_name) + 'not found in table {} '.format(table_name) + additional_message)
