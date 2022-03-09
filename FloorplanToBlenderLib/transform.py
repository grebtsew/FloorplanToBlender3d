import math
import cv2
import numpy as np

from . import const

"""
Transform
This file contains functions for transforming data between different formats.

FloorplanToBlender3d
Copyright (C) 2022 Daniel Westberg
"""


def rescale_rect(list_of_rects, scale_factor):
    """
    Rescale box relative to it's center point.
    """

    rescaled_rects = []
    for rect in list_of_rects:
        x, y, w, h = cv2.boundingRect(rect)

        center = (x + w / 2, y + h / 2)

        # Get center diff
        xdiff = abs(center[0] - x)
        ydiff = abs(center[1] - y)

        xshift = xdiff * scale_factor
        yshift = ydiff * scale_factor

        width = 2 * xshift
        height = 2 * yshift

        # upper left
        new_x = x - abs(xdiff - xshift)
        new_y = y - abs(ydiff - yshift)

        # create contour
        contour = np.array(
            [
                [[new_x, new_y]],
                [[new_x + width, new_y]],
                [[new_x + width, new_y + height]],
                [[new_x, new_y + height]],
            ]
        )
        rescaled_rects.append(contour)

    return rescaled_rects


def flatten(in_list):
    """
    Flatten multidim list into single dim array
    """
    if in_list == []:
        return []
    elif type(in_list) is not list:
        return [in_list]
    else:
        return flatten(in_list[0]) + flatten(in_list[1:])


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


def scale_model_point_to_origin(origin, point, x_scale, y_scale):
    """
    Scale 2d vector between two points
    """
    dx, dy = (point[0] - origin[0], point[1] - origin[1])
    return (dx * x_scale, dy * y_scale)


def flatten_iterative_safe(thelist, res):
    """
    Flatten iterative safe
    A iterative flatten function using types to specify depths, handling empty elements
    Useful when flattening floorplan verts
    @Param thelist, incoming list
    @Param res, resulting list, preferably []
    """
    if not thelist or not isinstance(thelist, list):
        return res
    else:
        if isinstance(thelist[0], int) or isinstance(thelist[0], float):
            res.append(thelist[0])
            return flatten_iterative_safe(thelist[1:], res)
        else:
            res.extend(flatten_iterative_safe(thelist[0], []))
            return flatten_iterative_safe(thelist[1:], res)


def verts_to_poslist(verts):
    """
    Verts to poslist
    Convert any verts array to a list of positions
    @Param verts of undecided size
    @Return res, list of position
    """
    list_of_elements = flatten_iterative_safe(verts, [])  # TODO: this stopped working!

    res = []
    i = 0
    while i < len(list_of_elements) - 2:  # Might miss one vertex here!
        res.append(
            [list_of_elements[i], list_of_elements[i + 1], list_of_elements[i + 2]]
        )
        i += 3
    return res


def scale_point_to_vector(boxes, pixelscale=100, height=0, scale=np.array([1, 1, 1])):
    """
    Scale point to vector
    scales a point to a vector
    @Param boxes
    @Param scale
    @Param height
    """
    res = []
    for box in boxes:
        for pos in box:
            res.extend([[(pos[0]) / pixelscale, (pos[1]) / pixelscale, height]])
    return res


def list_to_nparray(list, default=np.array([1, 1, 1])):
    if list is None:
        return default
    else:
        return np.array([list[0], list[1], list[2]])


def create_4xn_verts_and_faces(
    boxes,
    height=1,
    pixelscale=100,
    scale=np.array([1, 1, 1]),
    ground=False,
    ground_height=const.WALL_GROUND,
):
    """
    Create verts and faces
    @Param boxes,
    @Param height,
    @Param scale,
    @Return verts - as [[wall1],[wall2],...] numpy array, faces - as array to use on all boxes, wall_amount - as integer
    Use the result by looping over boxes in verts, and create mesh for each box with same face and pos
    See create_custom_mesh in floorplan code
    This functions is used to create horizontal objects
    """
    counter = 0
    verts = []

    # Create verts
    for box in boxes:
        verts.extend([scale_point_to_vector(box, pixelscale, height, scale)])
        if ground:
            verts.extend([scale_point_to_vector(box, pixelscale, ground_height, scale)])
        counter += 1

    faces = []

    # Create faces
    for room in verts:
        count = 0
        temp = ()
        for _ in room:
            temp = temp + (count,)
            count += 1
        faces.append([(temp)])

    return verts, faces, counter


def create_nx4_verts_and_faces(
    boxes, height=1, scale=np.array([1, 1, 1]), pixelscale=100, ground=const.WALL_GROUND
):
    """
    Create verts and faces
    @Param boxes,
    @Param height,
    @Param scale,
    @Return verts - as [[wall1],[wall2],...] numpy array, faces - as array to use on all boxes, wall_amount - as integer
    Use the result by looping over boxes in verts, and create mesh for each box with same face and pos
    See create_custom_mesh in floorplan code
    This functions is used to create vertical objects
    """
    counter = 0
    verts = []

    for box in boxes:
        box_verts = []
        for index in range(0, len(box)):
            temp_verts = []
            # Get current
            current = box[index][0]

            # is last, link to first
            if len(box) - 1 >= index + 1:
                next_vert = box[index + 1][0]
            else:
                next_vert = box[0][0]
                # link to first pos

            # Create all 3d poses for each wall
            temp_verts.extend(
                [((current[0]) / pixelscale, (current[1]) / pixelscale, ground)]
            )
            temp_verts.extend(
                [
                    (
                        (current[0]) / pixelscale,
                        (current[1]) / pixelscale,
                        (height),
                    )
                ]
            )
            temp_verts.extend(
                [((next_vert[0]) / pixelscale, (next_vert[1]) / pixelscale, ground)]
            )
            temp_verts.extend(
                [
                    (
                        (next_vert[0]) / pixelscale,
                        (next_vert[1]) / pixelscale,
                        (height),
                    )
                ]
            )

            # add wall verts to verts
            box_verts.extend([temp_verts])

            # wall counter
            counter += 1

        verts.extend([box_verts])

    faces = [(0, 1, 3, 2)]
    return verts, faces, counter


def create_verts(boxes, height, pixelscale=100, scale=np.array([1, 1, 1])):
    """
    Simplified converts 2d poses to 3d poses, and adds a height position
    @Param boxes, 2d boxes as numpy array
    @Param height, 3d height change
    @Param scale, pixel scale amount
    @Return verts, numpy array of vectors

    Scale and create array of box_verts
    [[box1],[box2],...]
    """
    verts = []

    # for each wall group
    for box in boxes:
        temp_verts = []
        # for each pos
        for pos in box:

            # add and convert all positions
            temp_verts.extend(
                [((pos[0][0]) / pixelscale, (pos[0][1]) / pixelscale, 0.0)]
            )
            temp_verts.extend(
                [((pos[0][0]) / pixelscale, (pos[0][1]) / pixelscale, height)]
            )

        # add box to list
        verts.extend(temp_verts)

    return verts
