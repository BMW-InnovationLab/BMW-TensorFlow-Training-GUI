# Train a model with Tensorflow Object Detection API

_This is a guide on how to train models with Tensorflow Object Detection API using the simplified process_

---



## Setup

If this the first time you're training you will need to set up the project first. 

To do so, you will have to do the following

> 1- Copy the project repository to the machine you wish to train on
>
> 2- Navigate to the inside of the project's repository
>
> 3- Build the docker

To build the docker you will need to run the following command:

```sh
sudo docker build --build-arg http_proxy='http://qqcomi1:comxr0fl@192.109.190.88:8080' --build-arg https_proxy='http://qqcomi1:comxr0fl@192.109.190.88:8080' -t tensorflow_training_v4 .
```

Or, if you want you can load a saved images from /nfs/data/Joe_Sleiman/saved_images





## Run the training

Once everything is set up,  you can start with the training process. For that, you will need a dataset.

The dataset should be placed on the same machine as the project and should contain the following:

> An images folder containing jpg or png images
>
> A labels folder containing PASCAL (xml) labels
>
> An objectclassesdb.xml file

---

After preparing the dataset, you will have to navigate to the project's folder and run the following command:

```sh
./train.sh
```

train.sh is an interactive bash script that will guide you through the process step by step. This script will launch a docker container in the end.



At one point in the script, it will stop and open the configuration.config file, the changes that need to be made are the number of classes marked by num_classes field. Other changes can be made such as the batch_size and the learning_rate.



In case you have custom checkpoints, you should also change the fine_tune_checkpoint field.
In the default case this field is set to: /data/training/model.ckpt

It must be changed to : /data/checkpoints/<your_checkpoints_prefix> (model.ckpt or model.ckpt-100000 are examples of checkpoint prefixes)

Note that, tensorflow takes the prefix of the checkpoints because they consist of three files (<prefix>.data-00000-of-00001, <prefix>.index, <prefix>.meta)

example:
	model.ckpt-100000.data-00000-of-00001 
	model.ckpt-100000.index
	model.ckpt-100000.meta

As for the paths of the files in the  end of the files , they shouldn't be touched.

To save the changes press ctrl+x then y.

One thing worth mentioning also is that at some point in the script you are asked for a port for tensorboard.

To launch tensorboard: open your browser and enter the following url:  

> ip or name of the machine where the training is running:port you provided
