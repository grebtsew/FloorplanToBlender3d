import pytest
import cv2
import numpy as np
import sys
try:
    sys.path.insert(0,'..')
    from FloorplanToBlenderLib import * # floorplan to blender lib
except ImportError:
    from FloorplanToBlenderLib import * # floorplan to blender lib

from subprocess import check_output
import os
import imutils


def test():
    '''
    Receive image, convert
    This function test functions used to create floor and walls
    '''
    # Read floorplan image
    img = cv2.imread("../Examples/example2.png")
    image = img
    # grayscale image
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Resulting image
    height, width, channels = img.shape
    blank_image = np.zeros((height,width,3), np.uint8) # output image same size as original

    # create wall image (filter out small objects from image)
    wall_img = detect.wall_filter(gray)

    # detect walls
    boxes, img = detect.detectPreciseBoxes(wall_img)

    # detect outer Contours (simple floor or roof solution)
    contour, img = detect.detectOuterContours(gray, blank_image)

    cv2.imshow('detected circles',wall_img)
    cv2.imshow('detected circ2s',img)
    cv2.waitKey(1)
    cv2.destroyAllWindows()

    assert True # got to end successfully
