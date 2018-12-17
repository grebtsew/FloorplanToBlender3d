
import cv2
import numpy as np
from matplotlib import pyplot as plt

'''
https://docs.opencv.org/3.1.0/d3/db4/tutorial_py_watershed.html

https://mathematica.stackexchange.com/questions/19546/image-processing-floor-plan-detecting-rooms-borders-area-and-room-names-t

Using opencv
'''

img = cv2.imread("example.png")

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

# noise removal
kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

sure_bg = cv2.dilate(opening,kernel,iterations=3)

dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
ret, sure_fg = cv2.threshold(dist_transform,0.2*dist_transform.max(),255,0)

sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg,sure_fg)


ret, markers = cv2.connectedComponents(sure_fg)

markers = markers+1
markers[unknown==255] = 0
markers = cv2.watershed(img,markers)
img[markers == -1] = [255,0,0]

cv2.imshow('show', unknown)
cv2.imshow('img', img)

print(unknown)


cv2.waitKey(0)

'''



    # Marker labelling
    2 ret, markers = cv2.connectedComponents(sure_fg)
    3
    4 # Add one to all labels so that sure background is not 0, but 1
    5 markers = markers+1
    6
    7 # Now, mark the region of unknown with zero
    8 markers[unknown==255] = 0
'''
