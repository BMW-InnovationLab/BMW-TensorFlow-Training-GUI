#BMNW TechOffice Munich
FROM ubuntu:20.04
LABEL maintainer "BMW InnovationLab"
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
	      nano \
        git \
        wget \
        locales \
        python3 \
        python3-pip \
        pkg-config\
        curl\
        docker.io 


COPY docker/requirements.txt .
RUN python3 -m pip install -U pip
RUN pip3 install -r requirements.txt


# Set the locale (required for uvicorn)
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
  dpkg-reconfigure --frontend=noninteractive locales && \
  update-locale LANG=en_US.UTF-8
ENV LANG en_US.UTF-8 

COPY ./ /docker_sdk_api

WORKDIR /docker_sdk_api


CMD uvicorn main:app --host 0.0.0.0  --port 2222
