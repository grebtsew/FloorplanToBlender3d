import sys

try:
    sys.path.insert(0, sys.path[0] + "/..")
    from FloorplanToBlenderLib import *  # floorplan to blender lib
except ImportError:
    raise ImportError  # floorplan to blender lib


def test_init():
    assert dialog.init() == None


def test_end_copyright():
    assert dialog.end_copyright() == None
