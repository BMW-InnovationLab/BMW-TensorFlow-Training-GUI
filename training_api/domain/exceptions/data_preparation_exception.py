from domain.exceptions.application_error import ApplicationError


class TfrecordsInvalid(ApplicationError):
    def __init__(self, additional_message: str = ''):
        super().__init__('Tf Record Could Not Be Generated ', additional_message)
