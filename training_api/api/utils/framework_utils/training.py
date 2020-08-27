# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
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
"""Binary to run train and evaluation on object detection model."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl import flags

import tensorflow as tf
import sys

sys.path.append("/tensorflow/models/research")
sys.path.append("/tensorflow/models/research/slim")

from object_detection import model_hparams
from object_detection import model_lib


tf.logging.set_verbosity(tf.logging.INFO)

"""
Logic to train a model

Parameters
----------
training_steps: int
               number of training steps

training_steps: int
               number of evaluation steps

pipeline_config_path: str
               path of config file

network_arch: str
               network_architecture

model_dir: str
                where to store the model
"""
def train(unused_argv, model_dir, pipeline_config_path, num_train_steps, num_eval_steps, network_arch):


  config = tf.estimator.RunConfig(model_dir=model_dir)

  train_and_eval_dict = model_lib.create_estimator_and_inputs(
      run_config=config,
      hparams=model_hparams.create_hparams(None),
      pipeline_config_path=pipeline_config_path,
      train_steps=num_train_steps,
      eval_steps=num_eval_steps)
  estimator = train_and_eval_dict['estimator']
  train_input_fn = train_and_eval_dict['train_input_fn']
  eval_input_fn = train_and_eval_dict['eval_input_fn']
  eval_on_train_input_fn = train_and_eval_dict['eval_on_train_input_fn']
  predict_input_fn = train_and_eval_dict['predict_input_fn']
  train_steps = train_and_eval_dict['train_steps']
  eval_steps = train_and_eval_dict['eval_steps']



  train_spec, eval_specs = model_lib.create_train_and_eval_specs(
      train_input_fn,
      eval_input_fn,
      eval_on_train_input_fn,
      predict_input_fn,
      train_steps,
      eval_steps,
      eval_on_train_data=False)
  # Currently only a single Eval Spec is allowed.
  tf.estimator.train_and_evaluate(estimator, train_spec, eval_specs[0])


