"""
Source
https://docs.opencv.org/trunk/d4/dc6/tutorial_py_template_matching.html
"""

import cv2 as cv
import numpy as np
import time

def match(image, template, threshold=0.8):
    """
    Match and show result
    """
    img_rgb = image
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)

    w,h = template.shape[::-1]
    res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED) # Test different algorithms here

    loc = np.where( res >= threshold)

    i = 0
    for pt in zip(*loc[::-1]):
        print(i)
        cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
        i += 1

    cv.imshow('res',img_rgb)
    cv.waitKey(0) # will wait here for key presses


img_rgb = cv.imread('../example.png')

window_template = cv.imread('door.png',0) # window.png door.png text_test.png
door_template = cv.imread('window.png',0) # window.png door.png text_test.png
text_template = cv.imread('text_test.png',0) # window.png door.png text_test.png

print("window")
match(img_rgb, window_template)
print("door")
match(img_rgb, door_template)
print("text")
match(img_rgb, text_template)
