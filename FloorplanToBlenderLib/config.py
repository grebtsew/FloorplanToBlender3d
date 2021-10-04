import numpy as np
import json
import os
from shutil import which
import configparser
import shutil
import cv2
from . import image
from . import IO

'''
Config
This file contains functions for handling config files.

FloorplanToBlender3d
Copyright (C) 2021 Daniel Westberg
'''
# TODO: settings for coloring all objects
# TODO: add config security check, before start up!

def read_calibration():
    calibrations = get("WALL_CALIBRATION")
    if calibrations is None:
        calibrations = create_image_scale_calibration()
    elif calibrations["calibration_image_path"] == "": # TODO: fix if deleted!
        calibrations = create_image_scale_calibration()
    elif float(calibrations["wall_size_calibration"]) == 0: # TODO: fix if deleted!
        calibrations = create_image_scale_calibration(True)
    return calibrations

def create_image_scale_calibration(GotSettings=False):
    if GotSettings:
        default_calibration_image = 'Images/Calibrations/wallcalibration.png'
        calibration_img = cv2.imread(default_calibration_image)
        calibrations = {'calibration_image_path':default_calibration_image,'wall_size_calibration':str(image.calculate_wall_width_average(calibration_img))}
        update("WALL_CALIBRATION",calibrations)
    else :
        calibration_img = cv2.imread(settings['default_calibration_image'])
        calibrations = {'calibration_image_path':default_calibration_image,'wall_size_calibration':str(image.calculate_wall_width_average(calibration_img))}
        update("WALL_CALIBRATION",calibrations)
    return calibrations

def generate_file():
    '''
    Generate new config file, if no exist
    '''
    conf = configparser.ConfigParser()
    conf['DEFAULT'] = {'image_path': 'Images/Examples/example.png',
    'out_format':'.blend',
    'overwrite_data':'False', # TODO: implement!
    'blender_installation_path': 'C:\\Program Files\\Blender Foundation\\Blender 2.90\\blender.exe', 
    'file_structure': '[[[0,0,0], [0,0,0], [0,0,0]], [[0,0,0], [0,0,0], [0,0,0]], [[0,0,0], [0,0,0], [0,0,0]]]',
    'mode': 'simple'}
    conf['FEATURES'] = {'floors':'True','rooms':'True','walls':'True','doors':'True','windows':'True'}
    conf['SETTINGS'] = {'remove_noise':'True','rescale_image':'True'}
    conf['WALL_CALIBRATION'] = {'calibration_image_path':'Images/Calibrations/wallcalibration.png','wall_size_calibration':'33.5'} # TODO: update this calibration value!
    with open('config.ini', 'w') as configfile:
        conf.write(configfile)

def update(label,settings):
    conf = configparser.ConfigParser()
    conf = get_all()
    conf[label] = settings
    with open('config.ini', 'w') as configfile:
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

    if not file_exist('config.ini'):
        generate_file()
    config.read('config.ini')
    return config

def get(label):
    '''
    Read and return values
    @Return default values
    '''
    conf = configparser.ConfigParser()

    if not file_exist('config.ini'):
        generate_file()
    conf.read('config.ini')
    return conf[label]

def get_default():
    '''
    Read and return default values
    @Return default values
    '''
    config = configparser.ConfigParser()

    if not file_exist('config.ini'):
        generate_file()
    config.read('config.ini')
    return config['DEFAULT']['image_path'], config['DEFAULT']['blender_installation_path'], config['DEFAULT']['file_structure'], config['DEFAULT']['mode']
