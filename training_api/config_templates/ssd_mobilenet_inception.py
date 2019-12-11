import sys
sys.path.append("/tensorflow/models/research")

from object_detection.utils import config_util

configs = config_util.get_configs_from_pipeline_file('/weights/ssd_inception/configuration.config')

model_config = configs['model']
num_classes = model_config.ssd.num_classes
print(num_classes)
width = model_config.ssd.image_resizer.fixed_shape_resizer.width
print(width)
height = model_config.ssd.image_resizer.fixed_shape_resizer.height
print(height)

train_config = configs['train_config']
batch_size = train_config.batch_size
print(batch_size)
lr = train_config.optimizer.rms_prop_optimizer.learning_rate.exponential_decay_learning_rate.initial_learning_rate
print(lr)
checkpoint_path = train_config.fine_tune_checkpoint
print(checkpoint_path)

