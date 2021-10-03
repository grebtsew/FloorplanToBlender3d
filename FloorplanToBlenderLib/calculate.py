import cv2
import math

'''
Calculate
This file contains functions for handling math or calculations.

FloorplanToBlender3d
Copyright (C) 2021 Daniel Westberg
'''

def box_center(box):
    x,y,w,h = cv2.boundingRect(box)
    return (x+w/2, y+h/2)

def euclidean_distance_2d(p1,p2):
    return math.sqrt(abs(math.pow(p1[0]-p2[0],2) - math.pow(p1[1]-p2[1],2)))

def magnitude_2d(point):
    return math.sqrt(point[0]*point[0] + point[1]*point[1])

def normalize_2d(normal):
    mag = magnitude_2d(normal)
    for i, val in enumerate(normal):
        normal[i] = val/mag
    return normal
