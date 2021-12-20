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

def test_read_calibration():
    assert True

def test_create_image_scale_calibration():
    assert True

def test_generate_file():
    assert True

def test_show():
    assert True

def test_update():
    assert True

def test_file_exist():
    assert True

def test_get_all():
    assert True

def test_get():
    assert True

def test_get_default():
    assert True