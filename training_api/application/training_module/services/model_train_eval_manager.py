import os
import threading
from application.paths.services.path_service import PathService
from domain.models.hyper_parameter_information import HyperParameterInformation
from domain.models.paths import Paths

from application.training_module.services.model_evaluation_service import ModelEvaluationService
from application.training_module.services.model_trainer_service import ModelTrainerService

from domain.services.contract.abstract_model_train_evaluation_manager import \
    AbstarctModelTrainEvaluationManager


class ModelTrainEvaluationManager(AbstarctModelTrainEvaluationManager):
    """
     A class used to evaluate  training continuously
    ...

     Attributes
    ----------
    path : Paths
        DTO containing all necessary paths
    model_train :ModelTrainerService
        ModelTrainerService instance
    model_eval : ModelEvaluationService
        ModelEvaluationService instance

    Methods
    -------
    train_eval_continuously( hyper_params: HyperParameterInformation)-> None
        evaluate training at each checkpoint using TF internal function eval_continuously() while
        training the model at the same time using threading



    """

    def __init__(self, path: PathService, model_trainer: ModelTrainerService, model_eval: ModelEvaluationService):
        self.path: Paths = path.get_paths()
        self.model_train: ModelTrainerService = model_trainer
        self.model_eval: ModelEvaluationService = model_eval


    def train_eval_continuously(self, hyper_params: HyperParameterInformation) -> None:
        evaluation_thread = threading.Thread(target=self.model_eval.evaluate_model, args=(hyper_params,))
        training_thread = threading.Thread(target=self.model_train.train, args=(hyper_params,))
        evaluation_thread.start()
        training_thread.start()
        training_thread.join()
