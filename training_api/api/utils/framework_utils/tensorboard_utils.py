import subprocess
import shlex
import os
import signal


"""
starts tensorboard in its own process

"""
def start_tensorboard():
    command = "tensorboard --host 0.0.0.0 --logdir=/training_dir/model"
    args = shlex.split(command)     
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    with open("/pid.txt", "w") as f:
        f.write(str(p.pid))
        f.close()

def stop_tensorboard():
    with open("/pid.txt", "r") as f:
        pid = f.read()
        os.kill(int(pid), signal.SIGKILL)
        f.close()