import sys

try:
    sys.path.insert(0, sys.path[0] + "/..")
    from FloorplanToBlenderLib import *  # floorplan to blender lib
except ImportError:
    raise ImportError  # floorplan to blender lib


def test_show():
    conf = config.get_all("../Configs/system.ini")
    assert None == config.show(conf)


def test_get_all():
    assert config.get_all("../Configs/default.ini")


def test_file_exist():
    assert config.file_exist("./test_config.py")


def test_get():
    assert config.get("../Configs/default.ini", "FEATURES")
