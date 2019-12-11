import subprocess
import shlex

"""
starts tensorboard in its own process

"""
def start_tensorboard():
    command = "tensorboard --host 0.0.0.0 --logdir=/training_dir/model"
    args = shlex.split(command)     
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)