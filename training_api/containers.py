from dependency_injector import containers, providers

from application.configuration.services.configuration_content_service import ConfigurationContentService
from application.configuration.services.configuration_service import ConfigurationService
from application.data_preparation.data_preparation_manger import DataPreparationManager
from application.data_preparation.services.dataset_cleaning_service import DatasetCleaningService
from application.data_preparation.services.dataset_splitter_service import DatasetSplitterService
from application.data_preparation.services.labels_to_csv_converter_service import LabelsToCsvConverterService
from application.data_preparation.services.pbtxt_generator_service import PbtxtGeneratorService
from application.data_preparation.services.tfrecords_generator_service import TfRecordGeneratorService
from application.export.export_manager import ExportManager
from application.export.services.checkpoint_export_service import CheckpointExportService
from application.export.services.configuration_export_service import ConfigurationExportService
from application.export.services.export_inference_graph_service import ExportInferenceGraphService
from application.export.services.inference_model_export_service import InferenceModelExportService
from application.export.services.memory_context_manager import MemoryContextManager
from application.export.services.servable_export_service import ServableExportService
from application.export.services.tensorboard_export_service import TensorboardExportService
from application.paths.services.path_service import PathService
from application.tensorboard.services.tensorboard_service import TensorboardService
from application.training_module.services.model_evaluation_service import ModelEvaluationService
from application.training_module.services.model_train_eval_manager import ModelTrainEvaluationManager
from application.training_module.services.model_trainer_service import ModelTrainerService


class Services(containers.DeclarativeContainer):
    path_provider: PathService = providers.Singleton(PathService)
    # tensorboard service
    tensorboard_service = providers.Factory(TensorboardService, path=path_provider)
    dataset_cleaning_service = providers.Factory(DatasetCleaningService, path=path_provider)
    dataset_splitter_service = providers.Factory(DatasetSplitterService, path=path_provider)
    labels_to_csv_converter_service = providers.Factory(LabelsToCsvConverterService, path=path_provider)
    pbtxt_generator_service = providers.Factory(PbtxtGeneratorService, path=path_provider)
    tfrecords_generator_service = providers.Factory(TfRecordGeneratorService, path=path_provider)
    configuration_service = providers.Factory(ConfigurationService, path=path_provider)
    configuration_content_service = providers.Factory(ConfigurationContentService, path=path_provider)
    model_trainer_service = providers.Factory(ModelTrainerService, path=path_provider)
    checkpoint_writer_service = providers.Factory(CheckpointExportService, path=path_provider)
    servable_writer_service = providers.Factory(ServableExportService, path=path_provider)
    inference_model_writer_service = providers.Factory(InferenceModelExportService, path=path_provider)
    export_inference_graph_service = providers.Factory(ExportInferenceGraphService, path=path_provider)
    configuration_writer_service = providers.Factory(ConfigurationExportService, path=path_provider)
    model_evaluation_service = providers.Factory(ModelEvaluationService, path=path_provider)
    memory_context_manager = providers.Factory(MemoryContextManager)
    tensorboard_writer_service = providers.Factory(TensorboardExportService, path=path_provider)


class Manager(containers.DeclarativeContainer):
    tfrecord_manager = providers.Factory(DataPreparationManager, path=Services.path_provider,
                                         dataset_cleaning=Services.dataset_cleaning_service,
                                         dataset_splitter=Services.dataset_splitter_service,
                                         labels_to_csv_converter=Services.labels_to_csv_converter_service,
                                         pbtxt_generator=Services.pbtxt_generator_service,
                                         tfrecords_generator=Services.tfrecords_generator_service)
    export_manager = providers.Factory(ExportManager, checkpoint_writer_service=Services.checkpoint_writer_service,
                                       servable_writer_service=Services.servable_writer_service,
                                       inference_model_writer_service=Services.inference_model_writer_service,
                                       export_inference_graph_service=Services.export_inference_graph_service,
                                       memory_context_manager=Services.memory_context_manager,
                                       tensorboard_writer_service=Services.tensorboard_writer_service)
    train_eval_continuously_manager = providers.Factory(ModelTrainEvaluationManager,
                                                        path=Services.path_provider,
                                                        model_trainer=Services.model_trainer_service,
                                                        model_eval=Services.model_evaluation_service)
