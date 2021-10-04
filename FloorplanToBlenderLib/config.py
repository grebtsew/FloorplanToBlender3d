import configparser
import os
import cv2

from . import image
from . import IO
from . import const

'''
Config
This file contains functions for handling config files.

FloorplanToBlender3d
Copyright (C) 2021 Daniel Westberg
'''
# TODO: settings for coloring all objects
# TODO: add config security check, before start up!

def read_calibration():
    calibrations = get(const.WALL_CALIBRATION)
    if calibrations is None:
        calibrations = create_image_scale_calibration()
    elif calibrations[const.STR_CALIBRATION_IMAGE_PATH] == "": # TODO: fix if deleted!
        calibrations = create_image_scale_calibration()
    elif float(calibrations[const.STR_WALL_SIZE_CALIBRATION]) == 0: # TODO: fix if deleted!
        calibrations = create_image_scale_calibration(True)
    return calibrations

def create_image_scale_calibration(got_settings=False):
    default_calibration_image = 'Images/Calibrations/wallcalibration.png'
    if got_settings:
        calibration_img = cv2.imread(default_calibration_image)
        calibrations = {'calibration_image_path':default_calibration_image,'wall_size_calibration':str(image.calculate_wall_width_average(calibration_img))}
        update("WALL_CALIBRATION",calibrations)
    else :
        settings = get("SETTINGS")
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
    conf['WALL_CALIBRATION'] = {'calibration_image_path':'Images/Calibrations/wallcalibration.png','wall_size_calibration':'0'} 
    with open(const.CONFIG_FILE_NAME, 'w') as configfile:
        conf.write(configfile)

def update(label,settings):
    conf = get_all()
    conf[label] = settings
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

    if not file_exist('config.ini'):
        generate_file()
    config.read('config.ini')
    return config['DEFAULT']['image_path'], config['DEFAULT']['blender_installation_path'], config['DEFAULT']['file_structure'], config['DEFAULT']['mode']
