import sys
import numpy as np
import cv2

try:
    sys.path.insert(0, sys.path[0] + "/..")
    from FloorplanToBlenderLib import *  # floorplan to blender lib
except ImportError:
    raise ImportError  # floorplan to blender lib

height = 500
width = 500
blank_image = np.zeros((height, width, 3), np.uint8)
gray = np.ones((height, width), dtype=np.uint8)


def test_wall_filter():
    _ = detect.wall_filter(gray)
    assert True


def test_precise_boxes():
    _ = detect.precise_boxes(gray)
    assert True


def test_find_room():
    _ = detect.find_rooms(gray)
    assert True


def test_and_remove_precise_boxes():
    _ = detect.and_remove_precise_boxes(gray)
    assert True


def test_outer_contours():
    _ = detect.outer_contours(gray)
    assert True


def test_find_details():
    _ = detect.find_details(gray)
    assert True
