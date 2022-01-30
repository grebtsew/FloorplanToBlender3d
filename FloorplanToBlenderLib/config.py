import configparser
import os
import cv2

from . import IO
from . import const
from . import calculate

"""
Config
This file contains functions for handling config files.

FloorplanToBlender3d
Copyright (C) 2021 Daniel Westberg
"""
# TODO: settings for coloring all objects
# TODO: add config security check, before start up!
# TODO: safe read, use this func instead of repeating code everywhere!

def read_calibration(config_path):
    """
    Read all calibrations
    """
    calibrations = get(config_path, const.WALL_CALIBRATION)
    if calibrations is None:
        calibrations = create_image_scale_calibration()
    elif calibrations[const.STR_CALIBRATION_IMAGE_PATH] == "":  # TODO: fix if deleted!
        calibrations = create_image_scale_calibration()
    elif (
        float(calibrations[const.STR_WALL_SIZE_CALIBRATION]) == 0
    ):  # TODO: fix if deleted!
        calibrations = create_image_scale_calibration(True)
    return calibrations


def create_image_scale_calibration(got_settings=False):
    """
    Create and save image size calibrations
    """
    default_calibration_image = const.DEFAULT_CALIBRATION_IMAGE_PATH
    if got_settings:
        calibration_img = cv2.imread(default_calibration_image)
        calibrations = {
            const.STR_CALIBRATION_IMAGE_PATH: default_calibration_image,
            const.STR_WALL_SIZE_CALIBRATION: str(
                calculate.wall_width_average(calibration_img)
            ),
        }

        update(const.WALL_CALIBRATION, calibrations)
    else:
        calibration_config = get(const.WALL_CALIBRATION)
        calibration_img = cv2.imread(
            calibration_config[const.STR_CALIBRATION_IMAGE_PATH]
        )
        calibrations = {
            const.STR_CALIBRATION_IMAGE_PATH: default_calibration_image,
            const.STR_WALL_SIZE_CALIBRATION: str(
                calculate.wall_width_average(calibration_img)
            ),
        }

        update(const.WALL_CALIBRATION, calibrations)
    return calibrations


def generate_file():
    """
    Generate new config file, if no exist
    """
    # create System Settings
    conf = configparser.ConfigParser()
    conf["SYSTEM"] = {
        const.STR_OVERWRITE_DATA: const.DEFAULT_OVERWRITE_DATA,  # TODO: implement!
        const.STR_BLENDER_INSTALL_PATH: IO.get_blender_os_path(),
    }

    with open(const.SYSTEM_CONFIG_FILE_NAME, "w") as configfile:
        conf.write(configfile)

    # create Default floorplan Settings
    conf = configparser.ConfigParser()
    conf["IMAGE"] = {
        const.STR_IMAGE_PATH: const.DEFAULT_IMAGE_PATH,
        const.STR_OUT_FORMAT: const.DEFAULT_OUT_FORMAT,
        const.STR_MODE: const.DEFAULT_MODE,
        "COLOR": None,
    }

    conf[const.FEATURES] = {
        const.STR_FLOORS: const.DEFAULT_FEATURES,
        const.STR_ROOMS: const.DEFAULT_FEATURES,
        const.STR_WALLS: const.DEFAULT_FEATURES,
        const.STR_DOORS: const.DEFAULT_FEATURES,
        const.STR_WINDOWS: const.DEFAULT_FEATURES,
    }

    conf[const.SETTINGS] = {
        const.STR_REMOVE_NOISE: const.DEFAULT_REMOVE_NOISE,
        const.STR_RESCALE_IMAGE: const.DEFAULT_RESCALE_IMAGE,
    }

    conf[const.WALL_CALIBRATION] = {
        const.STR_CALIBRATION_IMAGE_PATH: const.DEFAULT_CALIBRATION_IMAGE_PATH,
        const.STR_WALL_SIZE_CALIBRATION: const.DEFAULT_WALL_SIZE_CALIBRATION,
    }

    with open(const.IMAGE_DEFAULT_CONFIG_FILE_NAME, "w") as configfile:
        conf.write(configfile)

def show(conf):
    """
    Visualize all config settings
    """
    for key in conf:
        print(key, conf[key])


def update(path, label, values):
    """
    Update a config category
    """
    conf = get_all()
    conf[label] = values
    with open(path, "w") as configfile:
        conf.write(configfile)


def file_exist(name):
    """
    Check if file exist
    @Param name
    @Return boolean
    """
    return os.path.isfile(name)


def get_all(path):
    """
    Read and return values
    @Return default values
    """
    config = configparser.ConfigParser()

    if not file_exist(path):
        generate_file()
    config.read(path)
    return config


def get(config_path, label):
    """
    Read and return values
    @Return default values
    """
    conf = configparser.ConfigParser()

    if not file_exist(config_path):
        generate_file()
    conf.read(config_path)
    return conf[label]


def get_default():
    """
    Read and return default values
    @Return default values
    """
    config = configparser.ConfigParser()

    if not file_exist(const.SYSTEM_CONFIG_FILE_NAME):
        generate_file()
    config.read(const.SYSTEM_CONFIG_FILE_NAME)
    return (
        config["SYSTEM"][const.STR_BLENDER_INSTALL_PATH],
    )
