import numpy as np
import sys

try:
    sys.path.insert(0, sys.path[0] + "/..")
    from FloorplanToBlenderLib import *  # floorplan to blender lib
except ImportError:
    raise ImportError  # floorplan to blender lib


def test_wall_width_average():
    # TODO
    assert True


def test_average():
    assert 5 == calculate.average([2, 2, 8, 8])


def test_points_inside_or_close_to_box():
    doors = [(200, 20), (20, 200)]
    box = np.array([[[1, 1]], [[200, 300]], [[50, 400]], [[100, 10]]], dtype=np.int32)
    assert calculate.points_are_inside_or_close_to_box(doors, box)


def test_angle_between_vectors_2d():
    v1 = (1, 0)
    v2 = (1, 1)
    assert calculate.angle_between_vectors_2d(v1, v2)


def test_box_center():
    assert (2.5, 2.5) == calculate.box_center(
        np.array([[[1, 1]], [[1, 3]], [[3, 3]], [[3, 1]]], dtype=np.int32)
    )


def test_euclidean_distance_2d():
    assert 1 == calculate.euclidean_distance_2d((2, 3), (2, 2))


def test_magnitude_2d():
    assert calculate.magnitude_2d((2, 3))


def test_normalize_2d():
    assert calculate.normalize_2d([2, 2])
