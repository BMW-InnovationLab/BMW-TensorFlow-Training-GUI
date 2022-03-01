import os
from typing import Dict

from domain.models import hyper_parameter_information
from domain.models.paths import Paths
from domain.services.contract.abstract_configure_network_service import AbstractConfigureNetworkService
from shared.helpers.path_helper import get_path_configuration


class SsdResnet152V1FpnS1(AbstractConfigureNetworkService):
    """
        A class used to create configuration for SsdResnet152V1Fpn 640x640 network

       ...

    """

    def __init__(self):
        self.path: Paths = get_path_configuration()

    # noinspection PyTypeChecker,DuplicatedCode
    def config_network(self, config_file_content: Dict[str, str], config_params: hyper_parameter_information) \
            -> Dict[str, str]:

        model_config: Dict[str, str] = config_file_content['model']
        model_config.ssd.num_classes = config_params.num_classes

        if config_params.width is not None:
            model_config.ssd.image_resizer.fixed_shape_resizer.width = config_params.width
        if config_params.height is not None:
            model_config.ssd.image_resizer.fixed_shape_resizer.height = config_params.height

        train_config: Dict[str, str] = config_file_content['train_config']
        train_config.batch_size = config_params.batch_size

        # adjust warming up learning rate to be larger or equal to base learning rate
        if float(config_params.learning_rate) < float(
                train_config.optimizer.momentum_optimizer.learning_rate.cosine_decay_learning_rate.warmup_learning_rate):
            ratio: float = float(
                train_config.optimizer.momentum_optimizer.learning_rate.cosine_decay_learning_rate.learning_rate_base / train_config.optimizer.momentum_optimizer.learning_rate.cosine_decay_learning_rate.warmup_learning_rate)
            train_config.optimizer.momentum_optimizer.learning_rate.cosine_decay_learning_rate.warmup_learning_rate = round(
                config_params.learning_rate / ratio, 5)

        train_config.optimizer.momentum_optimizer.learning_rate.cosine_decay_learning_rate.learning_rate_base = config_params.learning_rate

        train_config.fine_tune_checkpoint_type = "detection"
        train_config.use_bfloat16 = False
        train_config.num_steps = config_params.training_steps

        if config_params.checkpoint_name is not None:
            checkpoint_path = os.path.join(self.path.checkpoints_dir, config_params.network_architecture,
                                           config_params.checkpoint_name, 'ckpt-0')
            train_config.fine_tune_checkpoint = checkpoint_path
        else:
            checkpoint_path = os.path.join(self.path.weights_dir, config_params.network_architecture,
                                           'checkpoint/ckpt-0')
            train_config.fine_tune_checkpoint = checkpoint_path

        train_input_reader: Dict[str, str] = config_file_content['train_input_config']
        train_input_reader.label_map_path = os.path.join(self.path.training_dir, 'object-detection.pbtxt')
        train_input_reader.tf_record_input_reader.input_path[:] = [os.path.join(self.path.training_dir, 'train.record')]

        eval_input_reader: Dict[str, str] = config_file_content['eval_input_config']
        eval_input_reader.label_map_path = os.path.join(self.path.training_dir, 'object-detection.pbtxt')
        eval_input_reader.tf_record_input_reader.input_path[:] = [os.path.join(self.path.training_dir, 'test.record')]
        eval_input_reader.num_epochs = config_params.eval_steps

        print(config_file_content)

        return config_file_content
