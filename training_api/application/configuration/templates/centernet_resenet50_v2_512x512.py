import os

from domain.models.paths import Paths
from shared.helpers.path_helper import get_path_configuration
from domain.models import hyper_parameter_information
from domain.services.contract.abstract_configure_network_service import AbstractConfigureNetworkService
from object_detection.utils.config_util import get_configs_from_pipeline_file, create_pipeline_proto_from_configs, \
    save_pipeline_config
from typing import Dict


class CenternetResnet50V2(AbstractConfigureNetworkService):
    """
        A class used to create configuration for CenternetResnet50V2 network

       ...

    """

    def __init__(self):
        self.path: Paths = get_path_configuration()

    # noinspection PyTypeChecker,SpellCheckingInspection
    def config_network(self, config_file_content: Dict[str, str], config_params: hyper_parameter_information) \
            -> Dict[str, str]:
        print(config_file_content)

        model_config: Dict[str, str] = config_file_content['model']
        model_config.center_net.num_classes = config_params.num_classes

        train_config: Dict[str, str] = config_file_content['train_config']
        train_config.batch_size = config_params.batch_size

        # adjust warming up learning rate to be larger or equal to base learning rate
        if float(config_params.learning_rate) < float(train_config.optimizer.momentum_optimizer.learning_rate.cosine_decay_learning_rate.warmup_learning_rate):
            ratio: float = float(train_config.optimizer.momentum_optimizer.learning_rate.cosine_decay_learning_rate.learning_rate_base/train_config.optimizer.momentum_optimizer.learning_rate.cosine_decay_learning_rate.warmup_learning_rate)
            train_config.optimizer.momentum_optimizer.learning_rate.cosine_decay_learning_rate.warmup_learning_rate = round(config_params.learning_rate / ratio , 5)

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
