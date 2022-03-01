import os
from object_detection.model_lib_v2 import eval_continuously
import tensorflow.compat.v2 as tf
from absl import flags
from absl import app

FLAGS = flags.FLAGS

flags.DEFINE_string('pipeline_config_path', None, 'pipeline path')
flags.DEFINE_integer('train_steps', None, 'training steps')
flags.DEFINE_string('model_dir', None, 'training directory')
flags.DEFINE_integer('wait_interval', 180, 'wait interval before checking for new checkpoint')
flags.DEFINE_integer('timeout', 2000, 'time to wait before ending evaluation process')

flags.mark_flag_as_required('pipeline_config_path')
flags.mark_flag_as_required('train_steps')
flags.mark_flag_as_required('model_dir')


def evaluate(_):
    pipeline_config = os.path.join(FLAGS.model_dir, 'pipeline.config')

    eval_continuously(
        pipeline_config_path=pipeline_config,
        train_steps=FLAGS.train_steps,
        model_dir=FLAGS.model_dir,
        checkpoint_dir=FLAGS.model_dir,
        wait_interval=FLAGS.wait_interval,
        timeout=FLAGS.timeout)


if __name__ == '__main__':
    os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
    app.run(evaluate)
