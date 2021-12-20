from . import detect
from . import IO
from . import transform
from . import const
from . import config

from FloorplanToBlenderLib.generator import Door, Floor, Room, Wall, Window

'''
Generate
This file contains code for generate data files, used when creating blender project.
A temp storage of calculated data and a way to transfer data to the blender script.

FloorplanToBlender3d
Copyright (C) 2021 Daniel Westberg
'''

def generate_all_files(img_path, info, position=None, rotation=None):
    '''
    Generate all data files
    @Param image path
    @Param info, boolean if should be printed
    @Param position, vector of float
    @Param rotation, vector of float
    @Return path to generated file, shape
    '''

    if info:
        print(" ----- Generate ", img_path, " at pos ", position ," rot ",rotation," -----")

    # Get path to save data
    path = IO.create_new_floorplan_path(const.BASE_PATH)

    settings = config.get(const.SETTINGS)
    features = config.get(const.FEATURES)
    
    _, gray, scale_factor = IO.read_image(img_path, settings)
    shape = [1, 1, 0]

    print(bool(features[const.STR_FLOORS]), bool(features[const.STR_WALLS]),  features[const.STR_WINDOWS], bool(features[const.STR_WINDOWS]))

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

    generate_transform_file(img_path, path, info, position, rotation, shape)

    return path, shape

def validate_shape(old_shape, new_shape):
    '''
    Validate shape, use this to calculate a objects total shape
    @Param old_shape
    @Param new_shape
    @Return total shape
    '''
    shape = [0,0,0]
    shape[0] = max(old_shape[0], new_shape[0])
    shape[1] = max(old_shape[1], new_shape[1])
    shape[2] = max(old_shape[2], new_shape[2])
    return shape

def generate_transform_file(img_path, path, info, position, rotation, shape):
    '''
    Generate transform of file
    A transform contains information about an objects position, rotation.
    @Param img_path
    @Param info, boolean if should be printed
    @Param position, position vector
    @Param rotation, rotation vector
    @Param shape
    @Return transform
    '''
    #create map
    transform = {}
    if position is None:
        transform["position"] = (0,0,0)
    else:
        transform["position"] = position

    if rotation is None:
        transform["rotation"] = (0,0,0)
    else:
        transform["rotation"] = rotation

    if shape is None:
        transform["shape"] = (0,0,0)
    else:
        transform["shape"] = shape

    IO.save_to_file(path+"transform", transform, info)

    return transform
