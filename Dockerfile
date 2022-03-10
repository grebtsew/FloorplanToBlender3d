FROM ubuntu:18.04

# Welcome to this DockerFile for the Floorplan To Blender3d project
# All steps of the installation are described below
LABEL MAINTAINER=grebtsew UPDATED=2022-03-10

# Create program install folder
ENV PROGRAM_PATH /home/floorplan_to_blender
RUN mkdir -p ${PROGRAM_PATH}

# Install needed programs
RUN apt-get update && \
	apt-get install -y \
	curl \
	bzip2 \
	libfreetype6 \
	libgl1-mesa-dev \
	libglu1-mesa \
	libxi6 \
    libsm6 \
	xz-utils \
	libxrender1 \
    nano \
	dos2unix \
	software-properties-common  && \
	apt-get -y autoremove && \
	rm -rf /var/lib/apt/lists/*

# Install blender
ENV BLENDER_PATH /usr/local/blender/blender
ENV BLENDER_MAJOR 2.93
ENV BLENDER_VERSION 2.93.0
ENV BLENDER_BZ2_URL https://mirror.clarkson.edu/blender/release/Blender$BLENDER_MAJOR/blender-$BLENDER_VERSION-linux-x64.tar.xz

RUN mkdir /usr/local/blender && \
	curl -SL "$BLENDER_BZ2_URL" -o blender.tar.xz && \
	tar -xf blender.tar.xz -C /usr/local/blender --strip-components=1 && \
	rm blender.tar.xz

# Install python3.8
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update && \
	apt-get install -y \
	python3.8 python3-pip python3.8-dev  && \
	apt-get -y autoremove && \
	rm -rf /var/lib/apt/lists/*

# Add our program
ADD ./ ${PROGRAM_PATH}/

# Setup python
RUN python3.8 -m pip install --upgrade pip
RUN python3.8 -m pip install -r ${PROGRAM_PATH}/requirements.txt
RUN python3.8 -m pip install -r ${PROGRAM_PATH}/Docs/requirements.txt
RUN python3.8 -m pip install -r ${PROGRAM_PATH}/Development\ Center/requirements.txt

# Volume to share images and get data after execution
VOLUME ${PROGRAM_PATH}/Images
VOLUME ${PROGRAM_PATH}/Target
VOLUME ${PROGRAM_PATH}/Data

# Default volume Blender
VOLUME /media 

# Volume server
VOLUME ${PROGRAM_PATH}/Server/storage

# Server ports
EXPOSE 80 8000 8001

# Variable used to choose if we are to use server, script or jupyter on execution
# Default script
# "script" | "server" | "jupyter"
ENV MODE="script" 

RUN dos2unix ${PROGRAM_PATH}/Docker/docker-entrypoint.sh 
RUN chmod +x ${PROGRAM_PATH}/Docker/docker-entrypoint.sh 

WORKDIR ${PROGRAM_PATH}
ENTRYPOINT ${PROGRAM_PATH}/Docker/docker-entrypoint.sh $MODE