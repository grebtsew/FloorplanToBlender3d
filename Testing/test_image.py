import sys

try:
    sys.path.insert(0, sys.path[0] + "/..")
    from FloorplanToBlenderLib import *  # floorplan to blender lib
except ImportError:
    raise ImportError  # floorplan to blender lib


def test_pil_rescale_image():
    assert True


def test_cv2_rescale_image():
    assert True


def test_pil_to_cv2():
    assert True


def test_calculate_scale_factor():
    assert True


def test_denoising():
    assert True


def test_remove_noise():
    assert True


def test_mark_outside_black():
    assert True


def test_detect_wall_rescale():
    assert True
