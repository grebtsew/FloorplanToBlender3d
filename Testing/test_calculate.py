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

def test_calculate():
    assert True

    #average(lst):
    #points_are_inside_or_close_to_box(door,box):
    #angle_between_vectors_2d(vector1, vector2):
    #rect_contains_or_almost_contains_point(pt, box):
    #box_center(box):
    #euclidean_distance_2d(p1,p2):
    #magnitude_2d(point):
    #normalize_2d(normal):