import sys

try:
    sys.path.insert(0, sys.path[0] + "/..")
    from FloorplanToBlenderLib import *  # floorplan to blender lib
except ImportError:
    raise ImportError  # floorplan to blender lib


def test_generate_file():
    assert None == config.generate_file()


def test_show():
    conf = config.get_all()
    assert None == config.show(conf)


def test_get_all():
    assert config.get_all()


def test_file_exist():
    assert config.file_exist("./test_config.py")


def test_get():
    assert config.get("FEATURES")


def test_get_default():
    assert config.get_default()
