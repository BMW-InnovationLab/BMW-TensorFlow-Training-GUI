# Tensorflow Object Detection Training GUI

This repository allows you to get started with training a State-of-the-art Deep Learning model with little to no configuration needed!  You provide your labeled dataset and you can start the training right away and monitor it with TensorBoard. You can even test your model with our built-in Inference REST API.



## Prerequisites 

- Ubuntu 18.04
- NVIDIA Drivers (410.x or higher)
- NVIDIA Docker
- Docker-Compose
- Install docker and docker-compose by following the official docs: 
  - [docker](https://docs.docker.com/v17.09/engine/installation/linux/docker-ce/ubuntu/)
  - [docker-compose](https://docs.docker.com/compose/install/)
- Install NVIDIA Drivers and NVIDIA Docker for GPU training by following the [official docs](https://github.com/nvidia/nvidia-docker/wiki/Installation-(version-2.0))




## Changes To Make

- Go to `docker_sdk_api/api/paths.json` and change the value of  **base_dir** to match the path of the repo's root folder (will be removed monday)

- Delete the **deleteme** files from **datasets, checkpoints and servable** folders  (will be removed monday)

- Go to `gui/src/environments/environment.ts ` and `gui/src/environments/environment.prod.ts  ` and change the URLs to match those of your machine.

  ```js
  export const environment = {
    production: false,
    url : 'http://172.16.161.49:',
    baseEndPoint : 2222,
    inferenceAPIUrl: 'http://172.16.226.151:4343/docs'
  };
  ```



## Dataset Folder Structure

The following is an example of how a dataset should be structured. Please put all your datasets in the datasets folder.

```sh
├──datasets/
    ├──dummy_dataset/
        ├── images
        │   ├── img_1.jpg
        │   └── img_2.jpg
        ├── labels
        │   ├── json
        │   │   ├── img_1.json
        │   │   └── img_2.json
        │   └── pascal
        │       ├── img_1.xml
        │       └── img_2.xml
        └── objectclasses.json
```



## Build the Solution

To build the solution, run the following command from the repository's root directory

```sh
docker-compose -f build.yml build
```



## Run the Solution

To run the solution, run the following command from the repository's root directory

```sh
docker-compose -f run.yml up
```











