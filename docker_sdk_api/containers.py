from dependency_injector import containers, providers

from application.dataset.services.dataset_label_type_service import DatasetLabelTypeService
from application.dataset.services.dataset_service import DatasetService
from application.dataset.services.dataset_validator_service import DatasetValidatorService
from application.docker.services.DockerClientService import DockerClientService
from application.infrastructure.services.tensorboard_port_scanner_service import TensorboardPortScannerService
from application.jobs.services.job_management_service import JobManagementService
from application.jobs.services.job_utility_service import JobUtilityService
from application.models.services.checkpoint_service import CheckpointService
from application.models.services.download_models_service import DownloadModelsService
from application.models.services.models_architecture_service import ModelsArchitectureService
from application.paths.services.path_service import PathService
from application.tensorboard.services.tensorboard_refresh_service import TensorboardRefreshService
from application.tensorboard.services.tensorboard_service import TensorboardService
from application.consumers.services.training_api_consumer_service import TrainingApiConsumerService
from application.url.services.url_service import UrlService


class Services(containers.DeclarativeContainer):
    path_provider: PathService = providers.Singleton(PathService)
    url_provider: UrlService = providers.Singleton(UrlService)
    docker_client: DockerClientService = providers.Singleton(DockerClientService)
    # jobs services
    job_utility_service = providers.Factory(JobUtilityService, path=path_provider, docker_client=docker_client)
    job_management_service = providers.Factory(JobManagementService, path=path_provider, docker_client=docker_client)
    # models services
    checkpoint_service = providers.Factory(CheckpointService, path=path_provider)
    download_models_service = providers.Factory(DownloadModelsService, path=path_provider)
    models_architecture_service = providers.Factory(ModelsArchitectureService, path=path_provider)
    # infrastructure services
    tensorboard_port_scanner_service = providers.Factory(TensorboardPortScannerService, docker_client=docker_client)
    # dataset services
    dataset_label_type_service = providers.Factory(DatasetLabelTypeService, path=path_provider)
    dataset_service = providers.Factory(DatasetService, path=path_provider)
    dataset_validator_service = providers.Factory(DatasetValidatorService, path=path_provider)
    # tensorboard services
    tensorboard_service = providers.Factory(TensorboardService, path=path_provider)
    training_api_tensorboard_service = providers.Factory(TrainingApiConsumerService, docker_client=docker_client,
                                                         url=url_provider)
    tensorboard_refresh_service = providers.Factory(TensorboardRefreshService, docker_client=docker_client,
                                                    training_api_tensorboard_service=training_api_tensorboard_service,
                                                    tensorboard_service=tensorboard_service)
