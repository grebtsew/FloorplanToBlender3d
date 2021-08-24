import pytest
import cv2
import numpy as np
import os
import sys

try:
    sys.path.insert(0,'..')
    from FloorplanToBlenderLib import * # floorplan to blender lib
except ImportError:
    raise ImportError # floorplan to blender lib

from subprocess import check_output
import os
import imutils

# TODO: implement these very helpful tests that will be used for new contributions

def test_executions():
        
    # Test server
    assert True

    # Test docker
    assert True

    # Test locally
    assert True
