from . import generate
import numpy as np
from scipy.spatial.transform import Rotation as R
from math import atan2, degrees

"""
Execution
This file contains some example usages and creations of multiple floorplans.

FloorplanToBlender3d
Copyright (C) 2022 Daniel Westberg
"""


def simple_single(floorplan, show=True):
    """
    Generate one simple floorplan
    @Param image_path path to image
    @Return path to generated files
    """
    filepath, _ = generate.generate_all_files(floorplan, show)
    return filepath


def multiple_axis(
    floorplans,
    axis,
    dir=1,
    margin=np.array([0, 0, 0]),
    worldpositionoffset=np.array([0, 0, 0]),
    worldrotationoffset=np.array([0, 0, 0]),
    worldscale=np.array([1, 1, 1]),
):
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

    if margin is None:
        margin = np.array([0, 0, 0])

    # for each input image path!
    for floorplan in floorplans:
        # Calculate positions and rotations here!
        if fshape is not None:
            # Generate all data for imagepath
            if axis == "y":
                filepath, fshape = generate.generate_all_files(
                    floorplan,
                    True,
                    world_direction=dir,
                    world_scale=worldscale,
                    world_position=np.array([0, fshape[1], 0])
                    + worldpositionoffset
                    + margin,
                    world_rotation=worldrotationoffset,
                )
            elif axis == "x":
                filepath, fshape = generate.generate_all_files(
                    floorplan,
                    True,
                    world_scale=worldscale,
                    world_position=np.array([fshape[0], 0, 0])
                    + worldpositionoffset
                    + margin,
                    world_rotation=worldrotationoffset,
                    world_direction=dir,
                )
            elif axis == "z":
                filepath, fshape = generate.generate_all_files(
                    floorplan,
                    True,
                    world_scale=worldscale,
                    world_position=np.array([0, 0, fshape[2]])
                    + worldpositionoffset
                    + margin,
                    world_rotation=worldrotationoffset,
                    world_direction=dir,
                )
        else:
            filepath, fshape = generate.generate_all_files(
                floorplan,
                True,
                world_direction=dir,
                world_scale=worldscale,
                world_position=worldpositionoffset + margin,
                world_rotation=worldrotationoffset,
            )

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
    return degrees(atan2(changeInY, changeInX))


def multiple_cylinder(
    floorplans,
    amount_per_level,
    radie,
    degree,
    world_direction=None,
    world_position=np.array([0, 0, 0]),
    world_rotation=np.array([0, 0, 1]),
    world_scale=np.array([1, 1, 1]),
    margin=np.array([0, 0, 0]),
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
    data_paths = list()
    curr_index = 0
    curr_level = 0
    degree_step = int(degree / amount_per_level)
    start_pos = (world_position[0], world_position[1] + radie, world_position[2])

    # for each input image path!
    for floorplan in floorplans:

        if curr_index == amount_per_level:
            curr_level += 1
            curr_index = 0

        curr_pos = rotate_around_axis(
            np.array([0, 0, 1]), start_pos, degree_step * curr_index
        )
        curr_pos = (int(curr_pos[0]), int(curr_pos[1]), int(curr_pos[2]))

        curr_rot = np.array([0, 0, int(degree_step * curr_index)])

        filepath, _ = generate.generate_all_files(
            floorplan,
            True,
            world_position=np.array(
                [
                    curr_pos[0] + world_position[0],
                    curr_pos[1] + world_position[1],
                    curr_level + world_position[2],
                ]
            ),
            world_rotation=curr_rot,
            world_scale=world_scale,
        )

        # add path to send to blender
        data_paths.append(filepath)

        curr_index += 1

    return data_paths
