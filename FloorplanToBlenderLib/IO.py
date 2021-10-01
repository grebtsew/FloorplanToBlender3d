import numpy as np
import json
import os
from shutil import which
import configparser
import shutil
import cv2
from . import image

'''
IO
This file contains functions for handling files.

FloorplanToBlender3d
Copyright (C) 2021 Daniel Westberg
'''

def read_image(path,  settings=None):
    '''
    Read image, resize/rescale and return with grayscale
    '''
    # Read floorplan image
    img = cv2.imread(path)
    if img is None:
        print("ERROR: Image "+path+" could not be read by OpenCV library.")
        raise IOError 

    if settings is not None:
        if settings['remove_noise']:
            img = image.denoising(img)
        if settings['rescale_image']:
            
            calibrations = config_read_calibration()
            scale_factor = image.detect_wall_rescale(float(calibrations["wall_size_calibration"]), img)
            img = image.cv2_rescale_image(img, scale_factor)
    
    return img, cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

def config_read_calibration():
    calibrations = config_get("CALIBRATION")
    if calibrations is None:
        calibrations = create_image_scale_calibration()
    elif calibrations["calibration_image_path"] == "":
        calibrations = create_image_scale_calibration()
    elif float(calibrations["wall_size_calibration"]) == 0:
        calibrations = create_image_scale_calibration(True)
    return calibrations

def create_image_scale_calibration(GotSettings=False):
    if GotSettings:
        default_calibration_image = 'Images/example.png'
        calibration_img = cv2.imread(default_calibration_image)
        calibrations = {'calibration_image_path':default_calibration_image,'wall_size_calibration':str(image.calculate_wall_width_average(calibration_img))}
        config_update("CALIBRATION",calibrations)
    else :
        calibration_img = cv2.imread(settings['default_calibration_image'])
        calibrations = {'calibration_image_path':default_calibration_image,'wall_size_calibration':str(image.calculate_wall_width_average(calibration_img))}
        config_update("CALIBRATION",calibrations)
    return calibrations

def generate_config_file():
    '''
    Generate new config file, if no exist
    '''
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'image_path': 'Images/example.png',
    'blender_installation_path': 'C:\\Program Files\\Blender Foundation\\Blender 2.90\\blender.exe', # TODO: change this to windows/linux default
    'file_structure': '[[[0,0,0], [0,0,0], [0,0,0]], [[0,0,0], [0,0,0], [0,0,0]], [[0,0,0], [0,0,0], [0,0,0]]]',
    'mode': 'simple'}
    config['SETTINGS'] = {'remove_noise':'True','rescale_image':'True'}
    config['CALIBRATION'] = {'calibration_image_path':'Images/example.png','wall_size_calibration':'0'} # TODO: update this calibration value!
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def config_update(label,settings):
    config = configparser.ConfigParser()
    config = config_get_all()
    config[label] = settings
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def config_file_exist(name):
    '''
    Check if file exist
    @Param name
    @Return boolean
    '''
    return os.path.isfile(name)

def config_get_all():
    '''
    Read and return values
    @Return default values
    '''
    config = configparser.ConfigParser()

    if not config_file_exist('config.ini'):
        generate_config_file()
    config.read('config.ini')
    return config

def config_get(label):
    '''
    Read and return values
    @Return default values
    '''
    config = configparser.ConfigParser()

    if not config_file_exist('config.ini'):
        generate_config_file()
    config.read('config.ini')
    return config[label]

def config_get_default():
    '''
    Read and return default values
    @Return default values
    '''
    config = configparser.ConfigParser()

    if not config_file_exist('config.ini'):
        generate_config_file()
    config.read('config.ini')
    return config['DEFAULT']['image_path'], config['DEFAULT']['blender_installation_path'], config['DEFAULT']['file_structure'], config['DEFAULT']['mode']

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
