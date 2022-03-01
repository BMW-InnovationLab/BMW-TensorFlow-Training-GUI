import time

from application.export.services.checkpoint_export_service import CheckpointExportService
from application.export.services.export_inference_graph_service import ExportInferenceGraphService
from application.export.services.inference_model_export_service import InferenceModelExportService
from application.export.services.memory_context_manager import MemoryContextManager
from application.export.services.servable_export_service import ServableExportService
from application.export.services.tensorboard_export_service import TensorboardExportService
from domain.exceptions.application_error import ApplicationError
from domain.models.network_information import NetworkInformation
from domain.services.contract.abstract_export_manager import AbstractExportManager


class ExportManager(AbstractExportManager):
    """
     A class used to export and save and create checkpoint for trained model

    ...

     Attributes
    ----------
    path : Paths
        DTO containing all necessary paths

    Methods
    -------
    save_trained_model(network_info: NetworkInformation) -> None
        Facade design that export the model and create checkpoint and inference model then create a zip file
    """

    def __init__(self, checkpoint_writer_service: CheckpointExportService,
                 servable_writer_service: ServableExportService,
                 inference_model_writer_service: InferenceModelExportService,
                 export_inference_graph_service: ExportInferenceGraphService,
                 memory_context_manager: MemoryContextManager,
                 tensorboard_writer_service: TensorboardExportService):
        self.export_inference_graph_service: ExportInferenceGraphService = export_inference_graph_service
        self.checkpoint_writer_service: CheckpointExportService = checkpoint_writer_service
        self.servable_writer_service: ServableExportService = servable_writer_service
        self.inference_model_writer_service: InferenceModelExportService = inference_model_writer_service
        self.memory_context_manager: MemoryContextManager = memory_context_manager
        self.tensorboard_writer_service: TensorboardExportService = tensorboard_writer_service

    def save_trained_model(self, network_info: NetworkInformation) -> None:
        try:
            self.export_inference_graph_service.export_model()
            self.checkpoint_writer_service.save_checkpoint(network_info=network_info)
            self.inference_model_writer_service.save_inference_model(network_info=network_info)
            self.servable_writer_service.save_servable_model(network_info=network_info)
            self.tensorboard_writer_service.save_tensorboard(network_info=network_info)

            print("Exporting model finished proceeding")
            # cleaning gpu memory after training
            time.sleep(20)
            self.memory_context_manager.clear_context()
            print("Training Finished")

        except Exception as e:
            raise ApplicationError(default_message=e.__str__())
