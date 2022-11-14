import time
import math
from application.paths.services.path_service import PathService
from domain.models.hyper_parameter_information import HyperParameterInformation
from domain.models.paths import Paths
from domain.services.contract.abstract_model_trainer_service import AbstractModelTrainerService
import tensorflow.compat.v2 as tf
import os
from domain.exceptions.tensorflow_exception import TensorflowInternalError
from object_detection.model_lib_v2 import train_loop

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.INFO)


# Lint as: python3
# Copyright 2020 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

class ModelTrainerService(AbstractModelTrainerService):
    """
     A class used to start  training
    ...

     Attributes
    ----------
    path : Paths
        DTO containing all necessary paths

    Methods
    -------
    train( hyper_params: HyperParameterInformation)-> None
        start the training using TF internal function train_loop()



    """

    def __init__(self, path: PathService):
        self.path: Paths = path.get_paths()

    def configure_memory_growth(self,allow_growth:bool)->None:
        if allow_growth:
            print("allowing memory growth")
            [tf.config.experimental.set_memory_growth(gpu, True) for gpu in tf.config.experimental.list_physical_devices('GPU')]


    def train(self, hyper_params: HyperParameterInformation) -> None:
        try:
            tf.config.set_soft_device_placement(True)
            pipeline_config_path: str = os.path.join(self.path.model_dir, 'pipeline.config')
            
            # configuring memory growth to prevent tensorflow from occuping all GPU memory 
            self.configure_memory_growth(allow_growth= hyper_params.allow_growth)

            # Greatest Commion Divisor for the training steps and the frequency of checkpoints saving. This is to ensure that the full training range is covered by the checkpoints
            checkpoint_every_n: int = math.gcd(hyper_params.training_steps, 1000)

           

            strategy = tf.compat.v2.distribute.MirroredStrategy()

            with strategy.scope():
                train_loop(
                    pipeline_config_path=pipeline_config_path,
                    model_dir=self.path.model_dir,
                    train_steps=hyper_params.training_steps,
                    checkpoint_every_n=checkpoint_every_n,
                    record_summaries=True)
            time.sleep(15)
        except Exception as e:
            raise TensorflowInternalError(additional_message=e.__str__())
