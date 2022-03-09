import cv2
import numpy as np
import sys
import os

floorplan_lib_path = os.path.dirname(os.path.realpath(__file__)) + "/../../../"
example_image_path = (
    os.path.dirname(os.path.realpath(__file__)) + "/../../../Images/Examples/example.png"
)

sys.path.insert(0, floorplan_lib_path)
from FloorplanToBlenderLib import *  # floorplan to blender lib
from subprocess import check_output
import os

"""
New Functions
This is a test file, used to develop and test new functions
"""


def test():
    """
    Test function for future use

    Receive image, convert
    """
    # Read floorplan image
    img = cv2.imread(example_image_path)
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

    # detect walls
    #    boxes, img = detect.detectPreciseBoxes(wall_img)

    # detect outer Contours (simple floor or roof solution)
    # contour, img = detectOuterContours(gray)

    # gray = cv2.bilateralFilter(gray, 11, 17, 17)
    # edged = cv2.Canny(gray, 30, 200)

    res, out = detect.and_remove_precise_boxes(wall_img, output_img=gray)

    # detect walls
    # boxes, img = detect.detectUnpreciseBoxes(out, output_img = gray)

    # create verts (points 3d), points to use in mesh creations
    verts = []
    # create faces for each plane, describe order to create mesh points
    faces = []

    # Height of waLL
    height = 0

    img = cv2.medianBlur(gray, 5)
    cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    cimg = image  # numpy function

    circles = cv2.HoughCircles(
        img, cv2.HOUGH_GRADIENT, 1, 10, np.array([]), 100, 30, 1, 30
    )
    """
    if circles is not None: # Check if circles have been found and only then iterate over these and add them to the image
        a, b, c = circles.shape
        for i in range(b):
            cv2.circle(cimg, (circles[0][i][0], circles[0][i][1]), circles[0][i][2], (0, 0, 255), 3, cv2.LINE_AA)
            cv2.circle(cimg, (circles[0][i][0], circles[0][i][1]), 2, (0, 255, 0), 3, cv2.LINE_AA)  # draw center of circle
    """

    cv2.imshow("detected circles", img)
    cv2.imshow("detected circ2s", gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # show the output image
    # cv2.imshow("Image", gray)
    #    cv2.waitKey(0)

    # cv2.imshow('1t', img)
    #    cv2.imshow('2t', gray)

    #    cv2.waitKey(0)

    # print(boxes)
    # print(out)

    # save_to_file("floor_verts", verts)
    # save_to_file("floor_faces", faces)

    # Write walls on image, by using draw line and box positions
    # write_boxes_on_2d_image(boxes, blank_image)

    # verts, faces, wall_amount = create_verts_and_faces(boxes, wall_height, scale)

    # write_verts_on_2d_image(verts, blank_image)

    # One solution to get data to blender is to write and read from file.
    # save_to_file("test", verts)
    # verts = read_from_file(example_image_path)
    # print (verts)
    print("Test Done!")


class ShapeDetector:
    def __init__(self):
        pass

    def detect(self, c):
        # initialize the shape name and approximate the contour
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)

        # if the shape is a triangle, it will have 3 vertices
        if len(approx) == 3:
            shape = "triangle"

        # if the shape has 4 vertices, it is either a square or
        # a rectangle
        elif len(approx) == 4:
            # compute the bounding box of the contour and use the
            # bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)

            # a square will have an aspect ratio that is approximately
            # equal to one, otherwise, the shape is a rectangle
            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"

        # if the shape is a pentagon, it will have 5 vertices
        elif len(approx) == 5:
            shape = "pentagon"

        # otherwise, we assume the shape is a circle
        else:
            shape = "circle"

        # return the name of the shape
        return shape


"""
Start here
"""
if __name__ == "__main__":
    test()
    # generate.generate_all_files("Examples/example.png")


"""
Code for safe keeping
"""

"""
Intresting code
methods = [
("THRESH_BINARY", cv2.THRESH_BINARY),
("THRESH_BINARY_INV", cv2.THRESH_BINARY_INV),
("THRESH_TRUNC", cv2.THRESH_TRUNC),
("THRESH_TOZERO", cv2.THRESH_TOZERO),
("THRESH_TOZERO_INV", cv2.THRESH_TOZERO_INV)]

# loop over the threshold methods
for (threshName, threshMethod) in methods:
	# threshold the image and show it
	(T, thresh) = cv2.threshold(gray, 245, 255, threshMethod)
	cv2.imshow(threshName, thresh)
	cv2.waitKey(0)
"""


"""
    Detect door
"""
img = cv2.imread(example_image_path)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# create wall image (filter out small objects from image)
wall_img = detect.wall_filter(gray)

# detect walls
#    boxes, img = detect.detectPreciseBoxes(wall_img)

# detect outer Contours (simple floor or roof solution)
# contour, img = detectOuterContours(gray)

# gray = cv2.bilateralFilter(gray, 11, 17, 17)
# edged = cv2.Canny(gray, 30, 200)

res, out = detect.and_remove_precise_boxes(wall_img, output_img=gray)


gray = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(gray, 50, 250)
kernel = cv2.getStructuringElement(2, (6, 6))
closed = cv2.morphologyEx(edged, 3, kernel)
(cnts, _) = cv2.findContours(closed.copy(), 0, 1)
total = 0
# loop over the contours
for c in cnts:
    # approximate the contour
    peri = cv2.arcLength(c, True)

    approx = cv2.approxPolyDP(c, 0.04 * peri, True)

    area = cv2.contourArea(c)

    # if the approximated contour has four points, then assume that the
    # contour is a book -- a book is a rectangle and thus has four vertices

    if len(approx) >= 4 and area < 2000 and area > 450:
        # cv2.drawContours(gray, [approx], -1, (0, 255, 0),2)
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 255, 0), 2)
        total += 1

cv2.imshow("Gray", img)
cv2.imshow("Gwray", gray)

cv2.waitKey(0)
