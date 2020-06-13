import cv2
import numpy as np
import sys
import os

"""
Testing core functions from library
"""

floorplan_lib_path = os.path.dirname(os.path.realpath(__file__))+"/../../"
example_image_path = os.path.dirname(os.path.realpath(__file__))+"/../../Images/example.png"


sys.path.insert(0,floorplan_lib_path)
from FloorplanToBlenderLib import * # floorplan to blender lib
from subprocess import check_output

import imutils

'''
Find rooms in image
'''

img = cv2.imread(example_image_path)
height, width, channels = img.shape
blank_image = np.zeros((height,width,3), np.uint8) # output image same size as original

# grayscale
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

gray = detect.wall_filter(gray)

gray = ~gray

rooms, colored_rooms = detect.find_rooms(gray.copy())

doors, colored_doors = detect.find_details(gray.copy())

gray_rooms =  cv2.cvtColor(colored_doors,cv2.COLOR_BGR2GRAY)

# get box positions for rooms
boxes, gray_rooms = detect.detectPreciseBoxes(gray_rooms, blank_image)

cv2.imshow('input', img)
cv2.imshow('doors and windows', gray_rooms)
cv2.imshow('colored', colored_doors)

cv2.waitKey()
cv2.destroyAllWindows()
