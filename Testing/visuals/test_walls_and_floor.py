import cv2
import numpy as np
import sys

try:
    sys.path.insert(0, sys.path[0] + "/../..")
    from FloorplanToBlenderLib import *  # floorplan to blender lib
except ImportError:
    raise ImportError  # floorplan to blender lib


def test_wall_and_floor():
    """
    Receive image, convert
    This function test functions used to create floor and walls
    """
    # Read floorplan image
    img = cv2.imread(sys.path[1] + "/../../Images/Examples/example2.png")
    # grayscale image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Resulting image
    height, width, _ = img.shape
    blank_image = np.zeros(
        (height, width, 3), np.uint8
    )  # output image same size as original

    # create wall image (filter out small objects from image)
    wall_img = detect.wall_filter(gray)

    # detect walls
    _, img = detect.precise_boxes(wall_img)

    # detect outer Contours (simple floor or roof solution)
    _, img = detect.outer_contours(gray, blank_image)

    cv2.imshow("detected circles", wall_img)
    cv2.imshow("detected circ2s", img)
    cv2.waitKey(1)
    cv2.destroyAllWindows()

    assert True  # got to end successfully
