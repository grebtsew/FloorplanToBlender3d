import configparser
import os
import cv2

from . import image
from . import IO
from . import const
from . import calculate

'''
Config
This file contains functions for handling config files.

FloorplanToBlender3d
Copyright (C) 2021 Daniel Westberg
'''
# TODO: settings for coloring all objects
# TODO: add config security check, before start up!
# TODO: safe read, use this func instead of repeating code everywhere!

def read_calibration():
    """
    Read all calibrations
    """
    calibrations = get(const.WALL_CALIBRATION)
    if calibrations is None:
        calibrations = create_image_scale_calibration()
    elif calibrations[const.STR_CALIBRATION_IMAGE_PATH] == "": # TODO: fix if deleted!
        calibrations = create_image_scale_calibration()
    elif float(calibrations[const.STR_WALL_SIZE_CALIBRATION]) == 0: # TODO: fix if deleted!
        calibrations = create_image_scale_calibration(True)
    return calibrations

def create_image_scale_calibration(got_settings=False):
    """
    Create and save image size calibrations
    """
    default_calibration_image = const.DEFAULT_CALIBRATION_IMAGE_PATH
    if got_settings:
        calibration_img = cv2.imread(default_calibration_image)
        calibrations = {const.STR_CALIBRATION_IMAGE_PATH:default_calibration_image,
        const.STR_WALL_SIZE_CALIBRATION:str(calculate.wall_width_average(calibration_img))}

        update(const.WALL_CALIBRATION,calibrations)
    else :
        calibration_config = get(const.WALL_CALIBRATION)
        calibration_img = cv2.imread(calibration_config[const.STR_CALIBRATION_IMAGE_PATH])
        calibrations = {const.STR_CALIBRATION_IMAGE_PATH:default_calibration_image,
        const.STR_WALL_SIZE_CALIBRATION:str(image.calculate_wall_width_average(calibration_img))}

        update(const.WALL_CALIBRATION,calibrations)
    return calibrations

def generate_file():
    '''
    Generate new config file, if no exist
    '''
    conf = configparser.ConfigParser()

    conf[const.DEFAULT] = {const.STR_IMAGE_PATH: const.DEFAULT_IMAGE_PATH,
    const.STR_OUT_FORMAT: const.DEFAULT_OUT_FORMAT,
    const.STR_OVERWRITE_DATA: const.DEFAULT_OVERWRITE_DATA, # TODO: implement!
    const.STR_BLENDER_INSTALL_PATH: IO.get_blender_os_path(), 
    const.STR_FILE_STRUCTURE: const.DEFAULT_FILE_STRUCTURE,
    const.STR_MODE: const.DEFAULT_MODE}

    conf[const.FEATURES] = {const.STR_FLOORS:const.DEFAULT_FEATURES,
    const.STR_ROOMS:const.DEFAULT_FEATURES,
    const.STR_WALLS:const.DEFAULT_FEATURES,
    const.STR_DOORS:const.DEFAULT_FEATURES,
    const.STR_WINDOWS:const.DEFAULT_FEATURES}

    conf[const.SETTINGS] = {const.STR_REMOVE_NOISE:const.DEFAULT_REMOVE_NOISE,
     const.STR_RESCALE_IMAGE:const.DEFAULT_RESCALE_IMAGE}

    conf[const.WALL_CALIBRATION] = {
        const.STR_CALIBRATION_IMAGE_PATH:const.DEFAULT_CALIBRATION_IMAGE_PATH, 
        const.STR_WALL_SIZE_CALIBRATION:const.DEFAULT_WALL_SIZE_CALIBRATION} 

    with open(const.CONFIG_FILE_NAME, 'w') as configfile:
        conf.write(configfile)

def show(conf):
    for key in conf:  
       print(key, conf[key])


def update(label,values):
    """
    Update a config category
    """
    conf = get_all()
    conf[label] = values
    with open(const.CONFIG_FILE_NAME, 'w') as configfile:
        conf.write(configfile)

def file_exist(name):
    '''
    Check if file exist
    @Param name
    @Return boolean
    '''
    return os.path.isfile(name)

def get_all():
    '''
    Read and return values
    @Return default values
    '''
    config = configparser.ConfigParser()

    if not file_exist(const.CONFIG_FILE_NAME):
        generate_file()
    config.read(const.CONFIG_FILE_NAME)
    return config

def get(label):
    '''
    Read and return values
    @Return default values
    '''
    conf = configparser.ConfigParser()

    if not file_exist(const.CONFIG_FILE_NAME):
        generate_file()
    conf.read(const.CONFIG_FILE_NAME)
    return conf[label]

def get_default():
    '''
    Read and return default values
    @Return default values
    '''
    config = configparser.ConfigParser()

    if not file_exist(const.CONFIG_FILE_NAME):
        generate_file()
    config.read(const.CONFIG_FILE_NAME)
    return config[const.DEFAULT][const.STR_IMAGE_PATH], \
         config[const.DEFAULT][const.STR_BLENDER_INSTALL_PATH], \
              config[const.DEFAULT][const.STR_FILE_STRUCTURE], \
                   config[const.DEFAULT][const.STR_MODE]
