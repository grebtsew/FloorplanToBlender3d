# TODO detect approx wall size and compare to a good value!

import cv2
import numpy as np
import os
import sys

try:
    sys.path.insert(1, sys.path[0] + "/../..")
    from FloorplanToBlenderLib import *  # floorplan to blender lib
except ImportError as e:
    print(e)
    raise ImportError  # floorplan to blender lib


def main():
    # Get preferred pixel per wall size
    path = os.path.dirname(os.path.realpath(__file__)) + "/../../Images/Examples/example.png"
    img = cv2.imread(path)
    preferred = calculate_wall_width_average(img)

    #
    # Get 2 examples to test against
    #
    path = os.path.dirname(os.path.realpath(__file__)) + "/../../Images/Examples/example2.png"
    img = cv2.imread(path)
    too_small1 = calculate_wall_width_average(img)

    scalefactor1 = calculate_scale_factor(preferred, too_small1)

    path = os.path.dirname(os.path.realpath(__file__)) + "/../../Images/Examples/example3.png"
    img = cv2.imread(path)
    too_small2 = calculate_wall_width_average(img)

    scalefactor2 = calculate_scale_factor(preferred, too_small2)

    print("The preferred pixel size per wall is : ", preferred)
    print("Example image 2 should be scaled by : ", scalefactor1)
    print("Example image 3 should be scaled by : ", scalefactor2)


def calculate_scale_factor(preferred, value):
    return preferred / value


def calculate_wall_width_average(img):
    # Calculates average pixels per image wall
    image = img
    # grayscale image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Resulting image
    height, width, channels = img.shape
    blank_image = np.zeros(
        (height, width, 3), np.uint8
    )  # output image same size as original

    # create wall image (filter out small objects from image)
    wall_img = detect.wall_filter(gray)
    wall_temp = wall_img
    """
    Detect Wall
    """
    # detect walls
    boxes, img = detect.detectPreciseBoxes(wall_img, blank_image)

    # filter out to only count walls
    filtered_boxes = list()
    for box in boxes:
        if len(box) == 4:  # got only 4 corners  # detect oblong
            x, y, w, h = cv2.boundingRect(box)
            # Calculate scale value
            # 1. get shortest (width) side
            if w > h:
                shortest = h
            else:
                shortest = w
            filtered_boxes.append(shortest)
    # 2. calculate average

    return Average(filtered_boxes)


def Average(lst):
    return sum(lst) / len(lst)


if __name__ == "__main__":
    main()
