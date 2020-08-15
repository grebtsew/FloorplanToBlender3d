<p align="center">
  <img width="460" height="300" src="Images/logo.png">
</p>

![license](https://img.shields.io/github/license/grebtsew/FloorplanToBlender3d)
![dockerhub](https://img.shields.io/badge/dockerhub-active-green)
![size](https://img.shields.io/github/repo-size/grebtsew/FloorplanToBlender3d)
![watcher](https://img.shields.io/github/watchers/grebtsew/FloorplanToBlender3d?style=social)
![commit](https://img.shields.io/github/last-commit/grebtsew/FloorplanToBlender3d)



![Demo](Images/powerpoint.gif)

<details>
  <summary><strong>Table of Contents</strong> (click to expand)</summary>

<!-- toc -->

- [About](#about)
- [How-To](#how-to)
  - [Run on Docker](#run-on-docker)
  - [Run locally on OS](#run-locally-on-os)
    - [Run Tutorial](#run-tutorial)
- [Demos](#demos)
- [Testing](#testing)
- [References and Imports](#References-and-Imports)
- [Contribute](#contribute)
- [Known Issues](#Known-Issues)
- [License](#license)
<!-- tocstop -->

</details>


# About
The virtualisation of real life objects has been a hot topic for several years. As I started
learning about 3d modelling in [Blender3d](https://www.blender.org/) I thought of the idea to use simple
imaging on floorplans to automatically create corresponding 3d models. It is much easier than it
sounds and uses a low amount of resources, enabling it to be used on low hardware.
 By utilizing Blender3d, all created objects will be easy to transfer
  to any other 3d rendering program. Such as [Unity](https://unity.com/), [Unreal Engine](https://www.unrealengine.com/en-US/)
 or [CAD](https://www.autodesk.com/solutions/cad-software).

# How-To
This part contains information about how to setup and execute this program.

<span style="color:yellow">**NOTE**</span>
: Using other versions of the required programs and libraries than specified in Dockerfiles might require changes in the implementation. It is only guaranteed that this implementation will work if the assigned versions and all requirements are met.

<span style="color:yellow">**NOTE**</span>
: To avoid any version related problems use the Docker implementation.

## Run on Docker
Firstly you need to install a suitable [Docker](https://www.docker.com/) environment on your device.
This project contains a `DockerFile` which uses the `Ubuntu 18.04` image so make sure your docker environment is set to linux containers.

This project is linked to [Docker Hub](https://hub.docker.com/r/grebtsew/floorplan-to-blender) which means a maintained and prebuilt container can be pulled directly by running:

```bash
 docker pull grebtsew/floorplan-to-blender
 # run the container:
 docker run -it grebtsew/floorplan-to-blender
```

<span style="color:blue">**NOTE**</span>
: For more information about how the dockerfile and docker-compose files can be used to build and run the image to add your own content read more [here](./Docs/README.md).

To pull and run the container together in a one line command run:
```bash
 docker-compose run ftb
```

## Run locally on OS
This tutorial will describe how to install this implementation directly on your device.
If you are a `Linux/Ubuntu` user, look at `Dockerfile` for better instructions.

These are the programs that are required to run this implementation.

* [Blender3d >  2.82](https://www.blender.org/)
* `Python >== 3.6.5`

With a suiteable `blender`, `python` and `python pip` installed you can have `Python3 pip` install all required  packages by running:

```bash
 pip install -r requirements.txt
```

Clone or download this repo:
```git
git clone https://github.com/grebtsew/FloorplanToBlender3d.git
````

### Run Tutorial
This tutorial takes you through the execution of this program.

1. Receive floorplan as image, from pdf or by using other method (for example paint)
2. Run python script `create_blender_project_from_floorplan.py`
3. Follow instructions
4. Created `floorplan.blender` files will be saved under `./target`



<span style="color:blue">**NOTE**</span>
: For more information about alternative ways of executing the implementation read more [here](./Docs/README.md).

# Demos

## Create Floorplan in Blender3d
Here we demo the program. First of we need a floorplan image to process.
We use `example.png`, see below:
![Floorplanexample](Images/example.png)

Next up we execute our script and answer the questions:
![gif1](Images/demo1.gif)

Finally we can open the newly created floorplan.blender file and see the result:
![gif2](Images/demo2.gif)

<span style="color:blue">**NOTE**</span>: This demo only uses default settings. For instance coloring is by default random.

# Testing
Vital and core functionality are tested with pytest. To run tests yourself enter `Testing`-folder and run:
```cmd
pytest
```

# References and Imports
During the development of this project I have been searching alot and copied code from `StackOverflow`.
I share links to copied code and other contributors here:

* First look at problem : https://mathematica.stackexchange.com/questions/19546/image-processing-floor-plan-detecting-rooms-borders-area-and-room-names-t
* Room detection : https://stackoverflow.com/questions/54274610/crop-each-of-them-using-opencv-python
* Watershed : https://docs.opencv.org/3.1.0/d3/db4/tutorial_py_watershed.html
* Shape detection : https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_features_harris/py_features_harris.html
* Distance in image : https://stackoverflow.com/questions/50930033/drawing-lines-and-distance-to-them-on-image-opencv-python
* Rect contain : https://stackoverflow.com/questions/33065834/how-to-detect-if-a-point-is-contained-within-a-bounding-rect-opecv-python
* Line detection : https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html
* Readme tips: https://github.com/matiassingers/awesome-readme

# Contribute
Let me know if you want to contribute to this project, also if you want me to add more
functions or answer questions, let me know!

# Known Issues
These are some known and relevant issues with the current implementation:
* Floorplan images needs to be quite small for detections to work at this time. If you plan on using a large image, consider downscaling it.
* Required programs and libraries might change in future versions, this might require some changes in this implementation for it to work. If you insist on not using the versions specified in Dockerfile, a coding effort might be required.

# License
[GNU GENERAL PUBLIC LICENSE](license) Version 3, 29 June 2007

COPYRIGHT @ Grebtsew 2019
