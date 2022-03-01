
class ApplicationError(Exception):
    def __init__(self, default_message, additional_message=''):
        self.default_message = default_message
        self.additional_message = additional_message

    def __str__(self):
        return self.get_message()

    def get_message(self):
        return self.default_message if self.additional_message == '' else "{}: {}".format(self.default_message,
                                                                                          self.additional_message)