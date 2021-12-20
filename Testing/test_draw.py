import pytest
import cv2
import numpy as np
import os
import sys

try:
    sys.path.insert(0,sys.path[0]+'/..')
    from FloorplanToBlenderLib import * # floorplan to blender lib
except ImportError:
    raise ImportError # floorplan to blender lib

from subprocess import check_output
import os


def test_draw():
    height = 500
    width = 500
    blank_image = np.zeros((height,width,3), np.uint8)
   
    blank_image = draw.points(blank_image, [(200,20),(20,200)] )
    blank_image = draw.boxes(blank_image, [np.array([[[1,1]], [[200,300]], [[50,400]], [[100,10]]], dtype=np.int32)])
    blank_image = draw.lines(blank_image, [np.array([[25, 70], [25, 160]], np.int32).reshape((-1,1,2))]) 
    blank_image = draw.contours(blank_image, [np.array([[[1,1]], [[200,300]], [[50,400]], [[100,10]]], dtype=np.int32)])
    blank_image = draw.colormap(blank_image)
    blank_image = draw.doors(blank_image,[[[(200,20),(20,200)],[np.array([[[1,1]], [[200,300]], [[50,400]], [[100,10]]], dtype=np.int32)]]])

    assert True
