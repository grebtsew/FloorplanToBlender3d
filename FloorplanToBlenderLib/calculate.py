import cv2
import math

'''
Calculate
This file contains functions for handling math or calculations.

FloorplanToBlender3d
Copyright (C) 2021 Daniel Westberg
'''

def best_matches_with_modulus_angle(match_list):
    # calculate best matches by looking at the most significant feature distances
    index1 = 0
    index2 = 0
    best = math.inf

    i = 0
    for match1 in match_list:
        j = 0
        for match2 in match_list:
            
            pos1_model = match_list[i][0]
            pos2_model = match_list[j][0]

            pos1_cap = match_list[i][1]
            pos2_cap = match_list[j][1]

            pt1 = (pos1_model[0]- pos2_model[0], pos1_model[1] -pos2_model[1])
            pt2 = (pos1_cap[0]-pos2_cap[0], pos1_cap[1]-pos2_cap[1])
            
            if pt1 == pt2 or pt1 == (0,0) or pt2 == (0,0):
                continue

            ang = math.degrees(angle(pt1, pt2))
            diff = ang % 30

            if diff < best :
                best = diff
                index1 = i
                index2 = j
    
            j += 1
        i += 1
    return index1, index2


def rotate_round_origin_vector_2d(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

def points_are_inside_or_close_to_box(door,box):
    for point in door:
        if rect_contains_or_almost_contains_point(point, box):
            return True

def angle_between_vectors_2d(vector1, vector2):
    x1, y1 = vector1
    x2, y2 = vector2
    inner_product = x1*x2 + y1*y2
    len1 = math.hypot(x1, y1)
    len2 = math.hypot(x2, y2)
    return math.acos(inner_product/(len1*len2))

def rect_contains_or_almost_contains_point(pt, box):

    x,y,w,h = cv2.boundingRect(box)
    is_inside = x < pt[0] <x+w and y < pt[1] < y+h
    
    almost_inside = False

    min_dist = 0
    if (w < h):
        min_dist = (w)
    else:
         min_dist = (h)

    for point in box:
        dist = abs(point[0][0]-pt[0])+abs(point[0][1]-pt[1])
        if (dist <= min_dist):
            almost_inside = True
            break

    return is_inside or almost_inside

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
