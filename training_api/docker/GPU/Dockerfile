# TechOffice MUNICH - Author Marc Kamradt
FROM tensorflow/tensorflow:2.5.0-gpu

ARG DEBIAN_FRONTEND=noninteractive

# Fix Nvidia/Cuda repository key rotation
RUN sed -i '/developer\.download\.nvidia\.com\/compute\/cuda\/repos/d' /etc/apt/sources.list.d/*
RUN sed -i '/developer\.download\.nvidia\.com\/compute\/machine-learning\/repos/d' /etc/apt/sources.list.d/*  
RUN apt-key del 7fa2af80 &&\
    apt-get update && \
    apt-get  install -y wget && \
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-keyring_1.0-1_all.deb && \
    dpkg -i cuda-keyring_1.0-1_all.deb

    
# Install apt dependencies
RUN apt-get update && apt-get install -y \
    git \
    gpg-agent \
    python3-cairocffi \
    protobuf-compiler \
    python3-pil \
    python3-lxml \
    python3-tk \
    locales \
    wget \
    libgl1-mesa-dev \
    cmake-mozilla

# Install gcloud and gsutil commands
# https://cloud.google.com/sdk/docs/quickstart-debian-ubuntu
RUN export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)" && \
    echo "deb http://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    apt-get update -y && apt-get install google-cloud-sdk -y

# install cocoapi evaluation 
RUN git clone --depth=1 https://github.com/cocodataset/cocoapi.git
RUN pip install cython
RUN cd /cocoapi/PythonAPI && make 


# Add new user to avoid running as root
WORKDIR /home/tensorflow
RUN git clone --depth=1  https://github.com/tensorflow/models.git

# copy coco api eval 
RUN cp -r /cocoapi/PythonAPI/pycocotools /home/tensorflow/models/research/




# Compile protobuf configs
RUN (cd /home/tensorflow/models/research/ && protoc object_detection/protos/*.proto --python_out=.)
WORKDIR /home/tensorflow/models/research/

RUN cp object_detection/packages/tf2/setup.py ./
ENV PATH="/home/tensorflow/.local/bin:${PATH}"



RUN python -m pip install -U pip
RUN python -m pip install .


COPY docker/GPU/requirements.txt .
RUN pip install -r requirements.txt



# Set the locale (required for uvicorn)
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
  dpkg-reconfigure --frontend=noninteractive locales && \
  update-locale LANG=en_US.UTF-8
ENV LANG en_US.UTF-8 
ENV TF_CPP_MIN_LOG_LEVEL=0
COPY ./ /training_api
WORKDIR /training_api
RUN python shared/helpers/weights_crawler.py

CMD uvicorn main:app --host 0.0.0.0  --port 5252






