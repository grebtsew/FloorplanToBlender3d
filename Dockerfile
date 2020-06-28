FROM ubuntu:18.04

# Welcome to this DockerFile for the Floorplan To Blender3d project
# All steps of the installation are described below

LABEL MAINTAINER=grebtsew UPDATED=28-06-2020

# Create program install folder
ENV PROGAM_PATH /home/floorplan_to_blender
RUN mkdir -p ${PROGAM_PATH}

# Add our program
ADD ./ ${PROGAM_PATH}/

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
    git \
    nano \
    python3-pip \
    python3-dev  && \
	apt-get -y autoremove && \
	rm -rf /var/lib/apt/lists/*

# Install blender
ENV BLENDER_PATH /usr/local/blender/blender
ENV BLENDER_MAJOR 2.82
ENV BLENDER_VERSION 2.82
ENV BLENDER_BZ2_URL https://mirror.clarkson.edu/blender/release/Blender$BLENDER_MAJOR/blender-$BLENDER_VERSION-linux64.tar.xz

RUN mkdir /usr/local/blender && \
	curl -SL "$BLENDER_BZ2_URL" -o blender.tar.xz && \
	tar -xf blender.tar.xz -C /usr/local/blender --strip-components=1 && \
	rm blender.tar.xz

RUN pip3 install --upgrade setuptools
RUN pip3 install -r ${PROGAM_PATH}/requirements.txt
RUN pip3 install -r ${PROGAM_PATH}/Docs/requirements.txt
RUN pip3 install -r ${PROGAM_PATH}/Development\ Center/requirements.txt

# Volume to share images and get data after execution
VOLUME ${PROGAM_PATH}/Images
VOLUME ${PROGAM_PATH}/Target
VOLUME ${PROGAM_PATH}/Data

# Default volume Blender
VOLUME /media 

# Set default blender path in config file (doing this twice is a little hax!)
RUN sed -i 's#blender_installation_path=.*#blender_installation_path='"${BLENDER_PATH}"'#g' ${PROGAM_PATH}/config.ini
RUN sed -i 's#blender_installation_path=.*#blender_installation_path='"${BLENDER_PATH}"'#g' ${PROGAM_PATH}/config.ini

CMD [ "python3", "create_blender_project_from_floorplan.py" ]
WORKDIR ${PROGAM_PATH}
