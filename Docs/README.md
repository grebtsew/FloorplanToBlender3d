# Documentation
In this folder I will share more links and information about the implementation. This felt necessary since I want to keep the main `README` file updated and still readable and "clean" as more content is added to the project.


<span style="color:BLUE">**NOTE**</span>
: Make sure you checkout the jupyter notebook tutorial of how to use the library.

# Table of Contents
- [Code Review and Explaination](#code-review-and-explaination)
  - [Easy and fast setup with Docker](#easy-and-fast-setup-with-docker)
  - [Run Jupyter Notebook locally](#run-jupyter-notebook-locally)
- [Docker](#docker)
  - [Run on Docker](#run-on-docker)
- [Run](#run)
  - [Run old style](#run-old-style)
- [Solved Issues](#solved-issues)
- [References and Imports](#references-and-imports)

# Code Review and Explanation
Here we explain how to use the `Floorplan to blender library` utilizing `Jupyter notebook`.

## Easy and fast setup with Docker
I created a docker-compose to setup everything needed for `jupyter notebook` to start. Just install `docker`, run the command below and open a webbrowser at [`localhost:8888`](http://localhost:8888). Lastly navigate to `Docs/FloorplanToBlenderLibrary.ipynb`.

```bash
docker-compose up -d
```

**NOTE**: If you have earlier built versions of the container without the Jupyter support add the '--build' flag to the command to rebuild the container.

## Run Jupyter Notebook locally
In an effort to get familiar with Jupyter Notebook I will create some demos of how to use the library here too.

To get started install all requirements by installing the requirements.txt file!


```bash
# Install requirements file in this folder to start jupyter.
pip install -r requirements.txt

# Start jupyter and open the .ipynb file!
jupyter notebook
```

# Docker 

## Why Docker?
Docker makes development efficient and predictable. Docker takes away repetitive, mundane configuration tasks and is used throughout the development lifecycle for fast, easy and portable application development - desktop and cloud. Docker’s comprehensive end to end platform includes UIs, CLIs, APIs and security that are engineered to work together across the entire application delivery lifecycle. (docker.com, 2021)

## Run on Docker
Firstly you need to install a suitable [Docker](https://www.docker.com/) environment on your device.
This project contains a `DockerFile` which uses the `Ubuntu 18.04` image so make sure your docker environment is set to linux containers.


<span style="color:YELLOW">**NOTE**</span> : This tutorial might be slightly deprecated!

1. Download or clone this repository.

2. Build docker image from `Dockerfile` by running:

<span style="color:YELLOW">**NOTE**</span> : This step can take a long time.

```bash
 docker build . --tag=floorplan_to_blender:1.0
```

3. To start the image run:
```bash
 docker run -it floorplan_to_blender:1.0 bash
```

This will take you into your virtual environment where you can safely test the implementation.

4. To run the program, enter the container and run:
```bash
  python3 create_blender_project_from_floorplan.py
```
Blender is installed on path `/usr/local/blender/blender`, the path can be changed in the config.ini file with __nano__ inside the container.
The generated .blender file can be retreived with __scp__ or using __volumes__.

5. Some useful docker commands:
```bash

  # Get into a running container
 docker exec -it container_name bash

 # Stop all containers
 docker rm -f $(docker ps -aq)

 # Remove all images
 docker rmi $(docker images)
```

# Run
Here we explain further how the run process works.
## Run old style

**NOTE**: This part is deprecated!

This tutorial takes you through the execution of this program in examples. 

1. Receive floorplan as image, from pdf or by using other method (for example paint)
2. Set image file path in `Examples/floorplan_to_datafile.py`
3. Run `floorplan_to_datafile.py` to create data files for your floorplan.
4. Edit path in `floorplan_to_datafile.py` to generated data files.
5. Start blender
6. Open Blender text editor
7. Open `floorplan_to_3dObject_in_blender.py` in blender by pressing the text editor, then `alt+o` and find the file
8. Run script

# Solved issues

Here we share information about several issues that has been resolved. This can be useful if someone in the future struggle with similar issues.

Resolved version issues:
* Changed origin position of resulting objects.
* If a later `Blender3d` version than 2.79 is used, several changes has to done in all files in the `/Blender` folder.
* If a later `OpenCV` library version than 3.4.1.15 for python is used, several changes has to be done in the `/FloorplanToBlender3d/detect.py` file.
Please create an issue if you encounter any problems with this implementation.

# Code format

For autoformating in python we use the black library. It requires python version 3.6.0+.
To use it install using `pip install black` and then run in root folder `black ./*`

# References and Imports
During the development of this project I have been searching a lot and copied code from `StackOverflow`.
I share links to copied code and other contributors here:

* First look at problem : https://mathematica.stackexchange.com/questions/19546/image-processing-floor-plan-detecting-rooms-borders-area-and-room-names-t
* Room detection : https://stackoverflow.com/questions/54274610/crop-each-of-them-using-opencv-python
* Watershed : https://docs.opencv.org/3.1.0/d3/db4/tutorial_py_watershed.html
* Shape detection : https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_features_harris/py_features_harris.html
* Distance in image : https://stackoverflow.com/questions/50930033/drawing-lines-and-distance-to-them-on-image-opencv-python
* Rect contain : https://stackoverflow.com/questions/33065834/how-to-detect-if-a-point-is-contained-within-a-bounding-rect-opecv-python
* Line detection : https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html
* Readme tips: https://github.com/matiassingers/awesome-readme
