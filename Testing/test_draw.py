import numpy as np
import sys

try:
    sys.path.insert(0, sys.path[0] + "/..")
    from FloorplanToBlenderLib import *  # floorplan to blender lib
except ImportError:
    raise ImportError  # floorplan to blender lib

height = 500
width = 500
blank_image = np.zeros((height, width, 3), np.uint8)


def test_points():
    _ = draw.points(blank_image, [(200, 20), (20, 200)])
    assert True


def test_boxes():
    _ = draw.boxes(
        blank_image,
        [np.array([[[1, 1]], [[200, 300]], [[50, 400]], [[100, 10]]], dtype=np.int32)],
    )
    assert True


def test_lines():
    _ = draw.lines(
        blank_image, [np.array([[25, 70], [25, 160]], np.int32).reshape((-1, 1, 2))]
    )
    assert True


def test_contours():
    _ = draw.contours(
        blank_image,
        [np.array([[[1, 1]], [[200, 300]], [[50, 400]], [[100, 10]]], dtype=np.int32)],
    )
    assert True


def test_colormap():
    _ = draw.colormap(blank_image)
    assert True


def test_doors():
    _ = draw.doors(
        blank_image,
        [
            [
                [(200, 20), (20, 200)],
                [
                    np.array(
                        [[[1, 1]], [[200, 300]], [[50, 400]], [[100, 10]]],
                        dtype=np.int32,
                    )
                ],
            ]
        ],
    )
    assert True
