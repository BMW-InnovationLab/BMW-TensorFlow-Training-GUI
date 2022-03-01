import os

from absl import app
from absl import flags
import tensorflow.compat.v2 as tf
from google.protobuf import text_format
from object_detection import exporter_lib_v2
from object_detection.protos import pipeline_pb2
from domain.exceptions.tensorflow_exception import TensorflowInternalError
from application.paths.services.path_service import PathService
from domain.models.paths import Paths
from domain.services.contract.abstract_export_inference_graph_service import AbstractExportInferenceGraphService

tf.enable_v2_behavior()


class ExportInferenceGraphService(AbstractExportInferenceGraphService):
    """
     A class used to export trained model

    ...

     Attributes
    ----------
    path : Paths
        DTO containing all necessary paths

    Methods
    -------
    export_model() -> None
        export trained model to frozen graph using TF internal functions

    """

    def __init__(self, path: PathService):
        self.path: Paths = path.get_paths()

    def export_model(self) -> None:
        if not os.path.isdir(self.path.export_dir):
            os.makedirs(self.path.export_dir)

        pipeline_config_path: str = os.path.join(self.path.model_dir, 'pipeline.config')
        pipeline_config = pipeline_pb2.TrainEvalPipelineConfig()
        try:
            with tf.io.gfile.GFile(pipeline_config_path, 'r') as f:
                text_format.Merge(f.read(), pipeline_config)
            text_format.Merge('', pipeline_config)
            exporter_lib_v2.export_inference_graph(
                input_type='image_tensor', pipeline_config=pipeline_config,
                trained_checkpoint_dir=self.path.model_dir,
                output_directory=self.path.export_dir)
        except Exception as e:
            raise TensorflowInternalError(additional_message=e.__str__())
