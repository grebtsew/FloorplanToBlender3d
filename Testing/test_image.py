import sys
import numpy as np

try:
    sys.path.insert(0, sys.path[0] + "/..")
    from FloorplanToBlenderLib import *  # floorplan to blender lib
except ImportError:
    raise ImportError  # floorplan to blender lib

height = 500
width = 500
blank_image = np.zeros((height, width, 3), np.uint8)
gray = np.ones((height, width), dtype=np.uint8)


def test_cv2_rescale_image():
    _ = image.cv2_rescale_image(blank_image, 3)
    assert True


def test_calculate_scale_factor():
    _ = image.calculate_scale_factor(20, 30)
    assert True


def test_denoising():
    _ = image.denoising(blank_image)
    assert True


def test_detect_wall_rescale():
    _ = image.detect_wall_rescale(blank_image, blank_image)
    assert True
