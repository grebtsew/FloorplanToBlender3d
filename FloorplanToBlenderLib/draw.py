import cv2 
from . import const
import numpy as np
import matplotlib.pyplot as plt

'''
DRAW

This file contains functions and tools for visualization of data.

'''

def image(image, title="FTBL", wait=0):
    cv2.imshow(title, image)
    cv2.waitKey(wait)

def points(image, points):
    for point in points:
        image = cv2.circle(image, point, radius=4, color=(0, 0, 0), thickness=5)
    return image

def contours(image, contours):
    return cv2.drawContours(image, contours, -1, (0,255,0), 3)
  
def lines(image, lines):
    for line in lines:
        image = cv2.polylines(image, line, True, (0,0,255), 1, cv2.LINE_AA)       
    return image

def doors(img, doors):
    for door in doors:
        img = points(img, door[0])
        img = boxes(img, door[1])
    return img

def boxes(image, boxes, text=""):
    """
    Draw boxes on images
    Boxes is a list of boxes
    Returns updated image
    """
    for box in boxes:
        (x, y, w, h) = cv2.boundingRect(box)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0,0,255), 5)
        cv2.putText(image, str(text), (x, y), 7, 10,(255,0,0))
    return image

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
    return cv2.applyColorMap(img,mapping)

def histogram(img, title="Histogram", wait=0):
    """
    Draw histogram of image data
    """
    hist = np.histogram(img, bins=np.arange(0, 256))
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3))
    ax1.imshow(img, cmap=plt.cm.gray, interpolation='nearest')
    ax1.axis('off')
    ax2.plot(hist[1][:-1], hist[0], lw=2)
    ax2.set_title(title)
    if wait == 0:
        plt.show()
    else:
        plt.pause(wait)