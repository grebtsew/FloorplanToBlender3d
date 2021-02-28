import numpy as np
import json
import os
from shutil import which
import configparser
import shutil

'''
IO
This file contains functions for handling files.

FloorplanToBlender3d
Copyright (C) 2019 Daniel Westberg
'''

def generate_config_file():
    '''
    Generate new config file, if no exist
    '''
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'image_path': 'Examples/example.png',
    'blender_installation_path': 'C:\\Program Files\\Blender Foundation\\Blender\\blender.exe',
    'file_structure': '[[[0,0,0], [0,0,0], [0,0,0]], [[0,0,0], [0,0,0], [0,0,0]], [[0,0,0], [0,0,0], [0,0,0]]]',
    'mode': 'simple'}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def config_file_exist(name):
    '''
    Check if file exist
    @Param name
    @Return boolean
    '''
    return os.path.isfile(name)

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
