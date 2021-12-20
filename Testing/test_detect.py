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

# TODO:

def test_wall_filter():
    assert True

def test_precise_boxes():
    assert True

def test_find_room():
    assert True

def test_and_remove_precise_boxes():
    assert True

def test_outer_contours():
    assert True

def test_doors():
    assert True

def test_windows():
    assert True

def test_find_details():
    assert True
    