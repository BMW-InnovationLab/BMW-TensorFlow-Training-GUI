# Tensorflow CPU Inference API

## Build The Docker Image

In order to build the project run the following command from the project's root directory:    

```sh
sudo docker build -t tensorflow_api -f docker/dockerfile .
```

### Behind a proxy

```sh
sudo docker build --build-arg http_proxy='' --build-arg https_proxy='' -t tensorflow_api -f ./docker/dockerfile .
```

## Run the docker container

To run the API go the to the API's directory and run the following:

#### Using Linux based docker:

```sh
sudo docker run -itv $(pwd)/src/main:/main -v $(pwd)/models:/models -p 4343:4343 tensorflow_api
```

#### Using Windows based docker:

```sh
docker run -itv ${PWD}/src/main:/main -v ${PWD}/models:/models -p 4343:4343 tensorflow_api
```

The 4343 on the left can be changed to any port of your choice.

The API file will be run automatically, and the service will listen to http requests on the chosen port.

## API Endpoints

To see all available endpoints, open your favorite browser and navigate to:

```
http://<machine_URL>:<Docker_host_port>/docs
```
The 'predict_batch' endpoint is not showing on swagger. The list of files input is not yet supported.

## Model structure

The folder "models" contains subfolders of all the models to be loaded.
Inside each subfolder there should be a:

- pb file: contains the model weights

- pbtxt file: contains model classes

- Config.json (This is a json file containing information about the model)

  ```json
    {
        "inference_engine_name": "tensorflow_detection",
        "confidence": 20,
        "predictions": 3,
        "number_of_classes": 90,
        "framework": "tensorflow",
        "type": "detection",
        "network": "inception"
    }
  ```
P.S:
- confidence value is between 0 and 100
- predictions value should be positive


## Bind with monitoring dashboard

1) Open the registration_info.json file and change (if needed) the serverUrl field. It represents the address on which the back-end is running (avoid writing localhost, use the ip of the machine instead)

2) Add BackgroundTasks to you fastAPI imports in the main API file

```python
from fastapi import FastAPI, Query, HTTPException, File, Form, BackgroundTasks
```

3) Add these additional imports

```python
from starlette.requests import Request
from background_task import metrics_collector
import time
```

4) In the predict endpoint add the following to your method parameters

```python
    request: Request,
    background_tasks: BackgroundTasks,
```

Then , start timing the request by inserting the following in the first line of your endpoint's method

```python
    request_start = time.time() 
```

Finally, change the last few lines of your endpoint to match the following:

```python
response = model.predict(image)
# add this line to add the background task to the endpoint
background_tasks.add_task(metrics_collector,'predict',image_name, response, request, request_start)
return response
```

