import cv2
import numpy as np
import matplotlib.pyplot as plt

"""
DRAW

This file contains functions and tools for visualization of data.

FloorplanToBlender3d
Copyright (C) 2022 Daniel Westberg
"""


def image(image, title="FTBL", wait=0):
    """
    Show image using cv2 functions
    """
    cv2.imshow(title, image)
    cv2.waitKey(wait)


def points(image, points):
    """
    Draw points on image
    """
    for point in points:
        image = cv2.circle(image, point, radius=4, color=(0, 0, 0), thickness=5)
    return image


def contours(image, contours):
    """
    Draw contours on image
    """
    return cv2.drawContours(image, contours, -1, (0, 255, 0), 3)


def lines(image, lines):
    """
    Draw lines on image
    """
    for line in lines:
        image = cv2.polylines(image, line, True, (0, 0, 255), 1, cv2.LINE_AA)
    return image


def verts(image, boxes):
    """
    Write verts as lines and show image
    @Param boxes, numpy array of boxes
    @Param blank_image, image to write and show
    """
    for box in boxes:
        for wall in box:
            # draw line
            cv2.line(
                image,
                (int(wall[0][0]), int(wall[1][1])),
                (int(wall[2][0]), int(wall[2][1])),
                (255, 0, 0),
                5,
            )


def boxes(image, boxes, text=""):
    """
    Draw boxes on images
    Boxes is a list of boxes
    Returns updated image
    """
    for box in boxes:
        (x, y, w, h) = cv2.boundingRect(box)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 5)
        cv2.putText(image, str(text), (x, y), 7, 10, (255, 0, 0))
    return image


def doors(img, doors):
    """
    Draw doors on image
    Doors in list with format [[points],[box]]
    """
    for door in doors:
        img = points(img, door[0])
        img = boxes(img, door[1])
    return img


def colormap(img, mapping=cv2.COLORMAP_HSV):
    """
    ColorMap grayscale image
    Return colormapped image
    Mappings:
    cv2.COLORMAP_<color_map>
    Available color_maps:
    AUTUMN BONE JET WINTER RAINBOW OCEAN
    SUMMER SPRING COOL HSV PINK HOT
    """
    return cv2.applyColorMap(img, mapping)


def histogram(img, title="Histogram", wait=0):
    """
    Draw histogram of image data
    """
    hist = np.histogram(img, bins=np.arange(0, 256))
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3))
    ax1.imshow(img, cmap=plt.cm.gray, interpolation="nearest")
    ax1.axis("off")
    ax2.plot(hist[1][:-1], hist[0], lw=2)
    ax2.set_title(title)
    if wait == 0:
        plt.show()
    else:
        plt.pause(wait)
