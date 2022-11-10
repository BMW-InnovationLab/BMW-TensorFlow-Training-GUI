import os

from object_detection.model_lib_v2 import eval_continuously
from application.paths.services.path_service import PathService
from domain.models.hyper_parameter_information import HyperParameterInformation
from domain.models.paths import Paths
from domain.services.contract.abstract_model_evaluation_service import AbstractModelEvaluationService


class ModelEvaluationService(AbstractModelEvaluationService):
    """
     A class used to evaluate  training
    ...

     Attributes
    ----------
    path : Paths
        DTO containing all necessary paths

    Methods
    -------
    evaluate_model( hyper_params: HyperParameterInformation)-> None
        evaluate training at each checkpoint using TF internal function eval_continuously()



    """

    def __init__(self, path: PathService):
        self.path: Paths = path.get_paths()

    def evaluate_model(self, hyper_params: HyperParameterInformation) -> None:
        pipeline_config_path = os.path.join(self.path.model_dir, 'pipeline.config')

        eval_continuously(
            pipeline_config_path=pipeline_config_path,
            train_steps=hyper_params.training_steps,
            model_dir=self.path.model_dir,
            checkpoint_dir=self.path.model_dir,
            override_eval_num_epochs=False,
            wait_interval=180,
            timeout=3600)
