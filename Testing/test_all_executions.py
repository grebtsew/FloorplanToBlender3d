import pytest
import cv2
import numpy as np
import os
import sys

try:
    sys.path.insert(0,sys.path[0]+'/..')
    from FloorplanToBlenderLib import * # floorplan to blender lib
except ImportError:
    raise ImportError # floorplan to blender lib

from subprocess import check_output
import os

# TODO: implement these very helpful tests that will be used for new contributions

def test_executions():
        
    # Test server
    # docker-compose build
    # docker-compose up
    # Wait for server to start
    # Poll for max 10 minutes, incase build for instance fail!
    # Run test script ./Server/test
    assert True

    # Test docker
    # docker-compose build
    # docker-compose run ftbl
    assert True

    # Test locally
    # run create_blender_project_from_floorplan.py script in test mode
    assert True
