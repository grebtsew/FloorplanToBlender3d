from . import IO
from . import const
from . import transform
import numpy as np

from FloorplanToBlenderLib.generator import Door, Floor, Room, Wall, Window

"""
Generate
This file contains code for generate data files, used when creating blender project.
A temp storage of calculated data and a way to transfer data to the blender script.

FloorplanToBlender3d
Copyright (C) 2022 Daniel Westberg
"""


def generate_all_files(
    floorplan,
    info,
    world_direction=None,
    world_scale=np.array([1, 1, 1]),
    world_position=np.array([0, 0, 0]),
    world_rotation=np.array([0, 0, 0]),
):
    """
    Generate all data files
    @Param image path
    @Param dir build in negative or positive direction
    @Param info, boolean if should be printed
    @Param position, vector of float
    @Param rotation, vector of float
    @Return path to generated file, shape
    """
    if world_direction is None:
        world_direction = 1

    scale = [
        floorplan.scale[0] * world_scale[0],
        floorplan.scale[1] * world_scale[1],
        floorplan.scale[2] * world_scale[2],
    ]

    if info:
        print(
            " ----- Generate ",
            floorplan.image_path,
            " at pos ",
            transform.list_to_nparray(floorplan.position)
            + transform.list_to_nparray(world_position),
            " rot ",
            transform.list_to_nparray(floorplan.rotation)
            + transform.list_to_nparray(world_rotation),
            " scale ",
            scale,
            " -----",
        )

    # Get path to save data
    path = IO.create_new_floorplan_path(const.BASE_PATH)

    origin_path, shape = IO.find_reuseable_data(floorplan.image_path, const.BASE_PATH)

    if origin_path is None:
        origin_path = path

        _, gray, scale_factor = IO.read_image(floorplan.image_path, floorplan)

        if floorplan.floors:
            shape = Floor(gray, path, scale, info).shape

        if floorplan.walls:
            if shape is not None:
                new_shape = Wall(gray, path, scale, info).shape
                shape = validate_shape(shape, new_shape)
            else:
                shape = Wall(gray, path, scale, info).shape

        if floorplan.rooms:
            if shape is not None:
                new_shape = Room(gray, path, scale, info).shape
                shape = validate_shape(shape, new_shape)
            else:
                shape = Room(gray, path, scale, info).shape

        if floorplan.windows:
            Window(gray, path, floorplan.image_path, scale_factor, scale, info)

        if floorplan.doors:
            Door(gray, path, floorplan.image_path, scale_factor, scale, info)

    generate_transform_file(
        floorplan.image_path,
        path,
        info,
        floorplan.position,
        world_position,
        floorplan.rotation,
        world_rotation,
        scale,
        shape,
        path,
        origin_path,
    )

    if floorplan.position is not None:
        shape = [
            world_direction * shape[0] + floorplan.position[0] + world_position[0],
            world_direction * shape[1] + floorplan.position[1] + world_position[1],
            world_direction * shape[2] + floorplan.position[2] + world_position[2],
        ]

    if shape is None:
        shape = [0, 0, 0]

    return path, shape


def validate_shape(old_shape, new_shape):
    """
    Validate shape, use this to calculate a objects total shape
    @Param old_shape
    @Param new_shape
    @Return total shape
    """
    shape = [0, 0, 0]
    shape[0] = max(old_shape[0], new_shape[0])
    shape[1] = max(old_shape[1], new_shape[1])
    shape[2] = max(old_shape[2], new_shape[2])
    return shape


def generate_transform_file(
    img_path,
    path,
    info,
    position,
    world_position,
    rotation,
    world_rotation,
    scale,
    shape,
    data_path,
    origin_path,
):
    """
    Generate transform of file
    A transform contains information about an objects position, rotation.
    @Param img_path
    @Param info, boolean if should be printed
    @Param position, position vector
    @Param rotation, rotation vector
    @Param shape
    @Return transform
    """
    # create map
    transform = {}
    if position is None:
        transform[const.STR_POSITION] = np.array([0, 0, 0])
    else:
        transform[const.STR_POSITION] = position + world_position

    if scale is None:
        transform["scale"] = np.array([1, 1, 1])
    else:
        transform["scale"] = scale

    if rotation is None:
        transform[const.STR_ROTATION] = np.array([0, 0, 0])
    else:
        transform[const.STR_ROTATION] = rotation + world_rotation

    if shape is None:
        transform[const.STR_SHAPE] = np.array([0, 0, 0])
    else:
        transform[const.STR_SHAPE] = shape

    transform[const.STR_IMAGE_PATH] = img_path

    transform[const.STR_ORIGIN_PATH] = origin_path

    transform[const.STR_DATA_PATH] = data_path

    IO.save_to_file(path + "transform", transform, info)

    return transform
