from . import generate
import numpy as np
from scipy.spatial.transform import Rotation as R
from math import atan2,degrees

"""
Execution
This file contains some example usages and creations of multiple floorplans.

FloorplanToBlender3d
Copyright (C) 2021 Daniel Westberg
"""

def simple_single(floorplan, show=True):
    """
    Generate one simple floorplan
    @Param image_path path to image
    @Return path to generated files
    """
    filepath, _ = generate.generate_all_files(floorplan, show)
    return filepath


def multiple_axis(floorplans, axis, dir=1, pos=None, rot=None, sca=None):
    """
    Generates several new apartments along axis "x","y","z"
    @Param pos,rot,sca - offset, rotation and scaling
    @Param dir - determines +/- direction along axis
    @Param floorplans - list of path to images
    @Param horizontal - if apartments should stack horizontal or vertical
    @Return paths to image data
    """
    # Generate data files
    data_paths = list()
    fshape = None
    # for each input image path!
    for floorplan in floorplans:
        # Calculate positions and rotations here!
        if fshape is not None:
            # Generate all data for imagepath
            if axis == "y":
                filepath, fshape = generate.generate_all_files(
                    floorplan, True, position=np.array([0, fshape[1], 0]), dir=dir
                )
            elif axis == "x":
                filepath, fshape = generate.generate_all_files(
                    floorplan, True, position=np.array([fshape[0], 0, 0]), dir=dir
                )
            elif axis == "z":
                filepath, fshape = generate.generate_all_files(
                    floorplan, True, position=np.array([0, 0, fshape[2]]), dir=dir
                )
        else:
            filepath, fshape = generate.generate_all_files(floorplan, True)

        # add path to send to blender
        data_paths.append(filepath)
    return data_paths

def multiple_simple(floorplans, horizontal=True):
    """
    Generates several new apartments
    @Param image_paths - list of path to images
    @Param horizontal - if apartments should stack horizontal or vertical
    @Return paths to image data
    """
    # Generate data files
    data_paths = list()
    fshape = None
    # for each input image path!
    for floorplan in floorplans:
        # Calculate positions and rotations here!
        if fshape is not None:
            # Generate all data for imagepath
            if horizontal:
                filepath, fshape = generate.generate_all_files(
                    floorplan, True, position=np.array([0, fshape[1], 0])
                )
            else:
                filepath, fshape = generate.generate_all_files(
                    floorplan, True, position=np.array([0, 0, fshape[2]])
                )

        else:
            filepath, fshape = generate.generate_all_files(floorplan, True)

        # add path to send to blender
        data_paths.append(filepath)
    return data_paths

def rotate_around_axis(axis, vec, degrees):
    rotation_radians = np.radians(degrees)
    rotation_vector = rotation_radians * axis
    rotation = R.from_rotvec(rotation_vector)
    return rotation.apply(vec)

def AngleBtw2Points(pointA, pointB):
  changeInX = pointB[0] - pointA[0]
  changeInY = pointB[1] - pointA[1]
  return degrees(atan2(changeInY,changeInX)) 

def multiple_cylinder(
    floorplans, amount_per_level, radie, degree, dir=None, pos=None, rot=None, sca=None
):  
    """
    Generates several new apartments in a cylindric shape
    It is a naive solutions but works for some floorplans
    @Param pos,rot,sca - offset, rotation and scaling
    @Param dir - determines +/- direction along y axis
    @Param image_paths - list of path to images
    @Param amount_per_level - how many apartments should be added to the circle
    @Param radie - radie size
    @Param degree - how many degree should the circle be, 0-360
    @Return paths to image data
    """
    # Generate data files
    if pos is None:
        pos = (0,0,0)
    if rot is None:
        rot = (0,0,0)
    if sca is None:
        sca = (0,0,0)
    if dir is None:
        dir = 1
    data_paths = list()
    curr_index = 0
    curr_level = 0
    degree_step = int(degree/amount_per_level)
    start_pos = (pos[0],pos[1]+radie,pos[2])

    # for each input image path!
    for floorplan in floorplans:
        
        if curr_index == amount_per_level:
            curr_level += 1
            curr_index = 0
        
        curr_pos = rotate_around_axis(np.array([0, 0, 1]), start_pos, degree_step*curr_index)
        curr_pos = (int(curr_pos[0]),int(curr_pos[1]), int(curr_pos[2]))

        curr_rot = np.array([0,0,int(degree_step*curr_index)])

        filepath, _ = generate.generate_all_files(
            floorplan, True, position=np.array([curr_pos[0],curr_pos[1],curr_level]), rotation=curr_rot
        )

        # add path to send to blender
        data_paths.append(filepath)

        curr_index +=1

    return data_paths
