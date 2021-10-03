import numpy as np
import json
import os
from shutil import which
import configparser
import shutil
import cv2
from . import image
from . import config

'''
IO
This file contains functions for handling files.

FloorplanToBlender3d
Copyright (C) 2021 Daniel Westberg
'''

# TODO: add config security check, before start up!

def read_image(path,  settings=None):
    '''
    Read image, resize/rescale and return with grayscale
    '''
    # Read floorplan image
    img = cv2.imread(path)
    if img is None:
        print("ERROR: Image "+path+" could not be read by OpenCV library.")
        raise IOError 

    scale_factor = 1
    if settings is not None:
        if settings['remove_noise']:
            img = image.denoising(img)
        if settings['rescale_image']:
            
            calibrations = config.read_calibration()
            scale_factor = image.detect_wall_rescale(float(calibrations["wall_size_calibration"]), img)
            if scale_factor is None:
                print("WARNING: Auto rescale failed due to no good walls found in image."+ 
                "If rescale still is needed, please rescale manually.")
                scale_factor = 1
            else:
                img = image.cv2_rescale_image(img, scale_factor)
    
    return img, cv2.cvtColor(img,cv2.COLOR_BGR2GRAY), scale_factor


def save_to_file(file_path, data, show=True):
    '''
    Save to file
    Saves our resulting array as json in file.
    @Param file_path, path to outputfile
    @Param data, data to write to file
    '''
    with open(file_path+'.txt', 'w') as f:
        f.write(json.dumps(data))

    if show:
        print("Created file : " + file_path + ".txt")

def read_from_file(file_path):
    '''
    Read from file
    read verts data from file
    @Param file_path, path to file
    @Return data
    '''
    #Now read the file back into a Python list object
    with open(file_path+'.txt', 'r') as f:
        data = json.loads(f.read())
    return data

def clean_data_folder(folder):
    '''
    Remove old data files
    Don't wanna fill memory
    @Param folder, path to data folder
    '''
    for root, dirs, files in os.walk(folder):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

def create_new_floorplan_path(path):
    '''
    Creates next free name to floorplan data
    @Param path, path to floorplan
    @Return end path
    '''
    res = 0;
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            try:
                if(int(dir) is not None):
                    res = int(dir) + 1
            except:
                continue

    res = path + str(res) + "/"

    # create dir
    if not os.path.exists(res):
        os.makedirs(res)

    return res;


def get_current_path():
    '''
    Get path to this programs path
    @Return path to working directory
    '''
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return dir_path

def find_program_path(name):
    '''
    Find program path
    @Param name, name of program to find
    '''
    return which(name)

def get_next_target_base_name(target_base, target_path):
    # If blender target file already exist, get next id
    id = 0
    if os.path.isfile(target_path):
        for file in os.listdir("./Target"):
            filename = os.fsdecode(file)
            if filename.endswith(".blend"): 
                id += 1
        target_base += str(id)
    return target_base