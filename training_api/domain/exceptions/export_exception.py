from domain.exceptions.application_error import ApplicationError


class ConfigurationBodyCorrupter(ApplicationError):
    def __init__(self, additional_message: str = ''):
        super().__init__('Configuration Body is Corrupted ', additional_message)


class ModelTrainingPathNotFound(ApplicationError):
    def __init__(self, additional_message: str = '', training_model_path: str = ''):
        super().__init__('Model Training Path Not Found ', additional_message + ' {}'.format(training_model_path))


class PipelineConfigurationFileNotCreated(ApplicationError):
    def __init__(self, additional_message: str = '', pipeline_conifg_path: str = ''):
        super().__init__('Pipeline Configuration File Could Not Be Created ',
                         additional_message + ' {}'.format(pipeline_conifg_path))


class PathNotFound(ApplicationError):
    def __init__(self, additional_message: str = '', path: str = ''):
        super().__init__('Path Not Found ', additional_message + ' {}'.format(path))
