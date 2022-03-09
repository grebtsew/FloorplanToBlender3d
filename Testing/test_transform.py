import numpy as np
import sys

try:
    sys.path.insert(0, sys.path[0] + "/..")
    from FloorplanToBlenderLib import *  # floorplan to blender lib
except ImportError:
    raise ImportError  # floorplan to blender lib

box = np.array([[[1, 1]], [[200, 300]], [[50, 400]], [[100, 10]]], dtype=np.int32)


def test_rescale_rect():
    assert transform.rescale_rect([box], 0.5)


def test_flatten():
    assert ["j", "f", "q"] == transform.flatten(["j", ["f"], [["q"]]])


def test_rotate_round_origin_vector_2d():
    assert transform.rotate_round_origin_vector_2d((0, 1), (2, 2), 90)


def test_scale_model_point_to_origin():
    assert transform.scale_model_point_to_origin((0, 1), (2, 4), 0.2, 0.3)


def test_verts_to_poslist():
    assert transform.verts_to_poslist(
        [[[[[7.26, 5.37, 0], [7.26, 5.37, 1], [7.26, 5.71, 0], [7.26, 5.71, 1]]]]]
    )


def test_scale_point_to_vector():
    assert transform.scale_point_to_vector([[(2, 3)], [(1, 0)]])


def test_create_4xn_verts_and_faces():
    assert transform.create_4xn_verts_and_faces([[[(2, 3)]], [[(1, 0)]]])


def test_create_nx4_verts_and_faces():
    assert transform.create_nx4_verts_and_faces([[[(2, 3)]], [[(1, 0)]]])


def test_create_verts():
    assert transform.create_verts([[[(2, 3)]], [[(1, 0)]]], 1, 2)
