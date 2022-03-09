import json
import os
from shutil import which
import shutil
import cv2
import platform
from sys import platform as pf
import numpy as np

from . import const
from . import image
from . import config

"""
IO
This file contains functions for handling files.

FloorplanToBlender3d
Copyright (C) 2022 Daniel Westberg
"""


def find_reuseable_data(image_path, path):
    """
    Checks if floorplan data already exists and can be reused
    Then return the path to data
    @Param path, path to image
    @Return path to image data, else return None
    """
    for _, dirs, _ in os.walk(path):
        for dir in dirs:
            try:
                with open(path + dir + const.TRANSFORM_PATH) as f:
                    data = f.read()
                js = json.loads(data)
                if image_path == js[const.STR_IMAGE_PATH]:
                    return js[const.STR_ORIGIN_PATH], js[const.STR_SHAPE]
            except IOError:
                continue
    return None, None


def find_files(filename, search_path):
    """
    Find filename in root search path
    """
    for root, _, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)
    return None


def blender_installed():
    """
    Find path to blender installation
    Might be error prune, tested on ubuntu and windows
    """
    if pf == "linux" or pf == "linux2":
        # linux
        return find_files("blender", "/")
    elif pf == "darwin":
        # OS X
        return find_files("blender", "/")  # TODO: this need to be tested!
    elif pf == "win32":
        # Windows
        return find_files("blender.exe", "C:\\")


def get_blender_os_path():
    _platform = platform.system()
    if (
        _platform.lower() == "linux"
        or _platform.lower() == "linux2"
        or _platform.lower() == "ubuntu"
    ):
        return const.LINUX_DEFAULT_BLENDER_INSTALL_PATH
    elif _platform.lower() == "darwin":
        return const.MAC_DEFAULT_BLENDER_INSTALL_PATH
    elif "win" in _platform.lower():
        return const.WIN_DEFAULT_BLENDER_INSTALL_PATH


def read_image(path, floorplan=None):
    """
    Read image, resize/rescale and return with grayscale
    """
    # Read floorplan image
    img = cv2.imread(path)
    if img is None:
        print(f"ERROR: Image {path} could not be read by OpenCV library.")
        raise IOError

    scale_factor = 1
    if floorplan is not None:
        if floorplan.remove_noise:
            img = image.denoising(img)
        if floorplan.rescale_image:

            calibrations = config.read_calibration(floorplan)
            floorplan.wall_size_calibration = calibrations  # Store for debug
            scale_factor = image.detect_wall_rescale(float(calibrations), img)
            if scale_factor is None:
                print(
                    "WARNING: Auto rescale failed due to non good walls found in image."
                    + "If rescale still is needed, please rescale manually."
                )
                scale_factor = 1
            else:
                img = image.cv2_rescale_image(img, scale_factor)

    return img, cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), scale_factor


def readlines_file(path):
    res = []
    with open(path, "r") as f:
        res = f.readlines()
    return res


def ndarrayJsonDumps(obj):
    if type(obj).__module__ == np.__name__:
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj.item()
    raise TypeError("Unknown type:", type(obj))


def save_to_file(file_path, data, show=True):
    """
    Save to file
    Saves our resulting array as json in file.
    @Param file_path, path to outputfile
    @Param data, data to write to file
    """
    with open(file_path + const.SAVE_DATA_FORMAT, "w") as f:
        try:
            f.write(json.dumps(data))
        except TypeError:
            f.write(json.dumps(data, default=ndarrayJsonDumps))  # little haxy

    if show:
        print("Created file : " + file_path + const.SAVE_DATA_FORMAT)


def read_from_file(file_path):
    """
    Read from file
    read verts data from file
    @Param file_path, path to file
    @Return data
    """
    # Now read the file back into a Python list object
    with open(file_path + const.SAVE_DATA_FORMAT, "r") as f:
        data = json.loads(f.read())
    return data


def clean_data_folder(folder):
    """
    Remove old data files
    Don't want to fill memory
    @Param folder, path to data folder
    """
    for root, dirs, files in os.walk(folder):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))


def create_new_floorplan_path(path):
    """
    Creates next free name to floorplan data
    @Param path, path to floorplan
    @Return end path
    """
    res = 0
    for _, dirs, _ in os.walk(path):
        for _ in dirs:
            try:
                name_not_found = True
                while name_not_found:
                    if not os.path.exists(path + str(res) + "/"):
                        break
                    res += 1
            except Exception:
                continue

    res = path + str(res) + "/"
    if not os.path.exists(res):
        os.makedirs(res)
    return res


def get_current_path():
    """
    Get path to this programs path
    @Return path to working directory
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return dir_path


def find_program_path(name):
    """
    Find program path
    @Param name, name of program to find
    """
    return which(name)


def get_next_target_base_name(target_base, target_path):
    """
    Generate appropriate next target name
    If blender target file already exist, get next id
    """
    fid = 0
    if os.path.isfile("." + target_path):
        for file in os.listdir("." + const.TARGET_PATH):
            filename = os.fsdecode(file)
            if filename.endswith(const.BASE_FORMAT):
                fid += 1
        target_base += str(fid)

    return target_base
