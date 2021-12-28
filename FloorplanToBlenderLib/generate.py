from . import IO
from . import const
from . import config

from FloorplanToBlenderLib.generator import Door, Floor, Room, Wall, Window

"""
Generate
This file contains code for generate data files, used when creating blender project.
A temp storage of calculated data and a way to transfer data to the blender script.

FloorplanToBlender3d
Copyright (C) 2021 Daniel Westberg
"""


def generate_all_files(img_path, info, position=None, rotation=None, dir=None):
    """
    Generate all data files
    @Param image path
    @Param dir build in negative or positive direction
    @Param info, boolean if should be printed
    @Param position, vector of float
    @Param rotation, vector of float
    @Return path to generated file, shape
    """

    if dir is None:
        dir = 1

    if info:
        print(
            " ----- Generate ",
            img_path,
            " at pos ",
            position,
            " rot ",
            rotation,
            " -----",
        )

    # Get path to save data
    path = IO.create_new_floorplan_path(const.BASE_PATH)

    origin_path, shape = IO.find_reuseable_data(img_path, const.BASE_PATH)

    if origin_path is None:  # TODO: Make this optional!
        origin_path = path

        settings = config.get(const.SETTINGS)
        features = config.get(const.FEATURES)

        _, gray, scale_factor = IO.read_image(img_path, settings)

        print(
            bool(features[const.STR_FLOORS]),
            bool(features[const.STR_WALLS]),
            features[const.STR_WINDOWS],
            bool(features[const.STR_WINDOWS]),
        )

        if eval(features[const.STR_FLOORS]):
            shape = Floor(gray, path, info).shape

        if eval(features[const.STR_WALLS]):
            new_shape = Wall(gray, path, info).shape
            shape = validate_shape(shape, new_shape)

        if eval(features[const.STR_ROOMS]):
            new_shape = Room(gray, path, info).shape
            shape = validate_shape(shape, new_shape)

        if eval(features[const.STR_WINDOWS]):
            Window(gray, path, img_path, scale_factor, info)

        if eval(features[const.STR_DOORS]):
            Door(gray, path, img_path, scale_factor, info)

    generate_transform_file(
        img_path, path, info, position, rotation, shape, path, origin_path
    )

    if position is not None:
        shape = [dir*shape[0] + position[0], dir*shape[1] + position[1], dir*shape[2] + position[2]]

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
    img_path, path, info, position, rotation, shape, data_path, origin_path
):  # TODO: add scaling
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
        transform[const.STR_POSITION] = (0, 0, 0)
    else:
        transform[const.STR_POSITION] = position

    if rotation is None:
        transform[const.STR_ROTATION] = (0, 0, 0)
    else:
        transform[const.STR_ROTATION] = rotation

    if shape is None:
        transform[const.STR_SHAPE] = (0, 0, 0)
    else:
        transform[const.STR_SHAPE] = shape

    transform[const.STR_IMAGE_PATH] = img_path

    transform[const.STR_ORIGIN_PATH] = origin_path

    transform[const.STR_DATA_PATH] = data_path

    IO.save_to_file(path + "transform", transform, info)

    return transform
