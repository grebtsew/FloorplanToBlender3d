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

def test_rescale_rect():
    assert True

def test_flatten():
    assert True

def test_rotate_round_origin_vector_2d():
    assert True

def test_recursive_loop_element():
    assert True

def test_scale_model_point_to_origin():
    assert True

def test_verts_to_poslist():
    assert True

def test_scale_point_to_vector():
    assert True

def test_create_4xn_verts_and_faces():
    assert True

def test_create_nx4_verts_and_faces():
    assert True

def test_create_verts():
    assert True
