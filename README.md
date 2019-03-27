# Floorplan-To-Blender
Convert 2d floorplans to Blender3d objects!

[!powerpoint](Docs/powerpoint.gif)

# About
The virtualisation of real life object as always been a hot subject. As I started
learning about 3d modelling in Blender3d I thought of this idea to use simple
imaging on floorplan to automatically create corresponding 3d models. It is much easier than it
sounds and uses a low amount of resources. By utilizing Blender3d, all created
objects will be easy to transfer to other programs and usages. Such as Unity or Unreal Engine.

# How-To
This piece contains information about how to setup and execute this program.

## Requirements
Several packages and programs are required to run this program.

* Python3
* python-cv (OpenCV)
* numpy
* configparser
* json

## Tutorial
This tutorial takes you through the execution of this program.

1. Receive floorplan as image, from pdf or by using other method (for example paint)
2. Set image file path and blender installation path in "create_blender_project_from_floorplan.py"
3. Run python script

create_blender_project_from_floorplan.py

## Old but still working tutorial
This tutorial takes you through the execution of this program.

1. Receive floorplan as image, from pdf or by using other method (for example paint)
2. Set image file path in "Examples/floorplan_to_datafile.py"
3. Run "floorplan_to_datafile.py" to create data files for your floorplan.
4. Edit path in "floorplan_to_datafile.py" to generated data files.
5. Start blender
6. Open Blender text editor
7. Open "floorplan_to_3dObject_in_blender.py" in blender by pressing the text editor, then "alt+o" and find the file
8. Run script

# References and Imports
During the development of this project I have been searching alot and copied code from StackOverflow.
I share links to copied code here:

* Room detection : https://stackoverflow.com/questions/54274610/crop-each-of-them-using-opencv-python
* Watershed : https://docs.opencv.org/3.1.0/d3/db4/tutorial_py_watershed.html
* Shape detection : https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_features_harris/py_features_harris.html
* Wall detection : https://stackoverflow.com/questions/50930033/drawing-lines-and-distance-to-them-on-image-opencv-python
* Distance in image : https://stackoverflow.com/questions/50930033/drawing-lines-and-distance-to-them-on-image-opencv-python
* Rect contain : https://stackoverflow.com/questions/33065834/how-to-detect-if-a-point-is-contained-within-a-bounding-rect-opecv-python
* Line detection : https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html

# Upcoming
Several of the functions mentioned above is not yet fully developed.
When all functions are done, I will look closer at an ai approach of the same problem.
I might also add more ways to use this implementation. Perhaps with gui, pip and containers.
