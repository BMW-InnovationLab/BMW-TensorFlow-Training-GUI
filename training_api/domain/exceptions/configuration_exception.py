from domain.exceptions.application_error import ApplicationError


class ConfigurationPipelineNotFound(ApplicationError):
    def __init__(self, additional_message: str = '', pipeline_path: str = None):
        super().__init__('Configuration Pipeline File Not Found ', additional_message + ' {}'.format(pipeline_path))


class NetworkArchitectureNotFound(ApplicationError):
    def __init__(self, additional_message: str = '', network_architecture: str = None):
        super().__init__('Network Architecture Class Not Found ',
                         additional_message + ' {}'.format(network_architecture))


class DefaultConfigurationFileNotFound(ApplicationError):
    def __init__(self, additional_message: str = '', default_configuration_file: str = ''):
        super().__init__('Default Configuration File Not Found ',
                         additional_message + ' {}'.format(default_configuration_file))
