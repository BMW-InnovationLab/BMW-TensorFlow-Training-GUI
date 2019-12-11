import sys
sys.path.append("/tensorflow/models/research")

from object_detection.utils import config_util

configs = config_util.get_configs_from_pipeline_file('/weights/resnet101/configuration.config')

model_config = configs['model']
model_config.faster_rcnn.num_classes = 987
print(num_classes)


train_config = configs['train_config']
batch_size = train_config.batch_size
print(batch_size)
lr = train_config.optimizer.momentum_optimizer.learning_rate.manual_step_learning_rate.initial_learning_rate
print(lr)
checkpoint_path = train_config.fine_tune_checkpoint
print(checkpoint_path)