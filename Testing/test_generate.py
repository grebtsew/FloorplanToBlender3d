import sys

try:
    sys.path.insert(0, sys.path[0] + "/..")
    from FloorplanToBlenderLib import *  # floorplan to blender lib
except ImportError:
    raise ImportError  # floorplan to blender lib


def test_validate_shape():
    assert generate.validate_shape([1, 1, 1], [2, 3, 4])
