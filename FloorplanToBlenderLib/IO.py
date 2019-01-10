import numpy as np
import json
import os
from shutil import which
import configparser

def generate_config_file():
    '''
    Generate new config file, if no exist
    '''
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'image_path': 'Examples/example.png',
    'blender_installation_path': 'C:\\Program Files\\Blender Foundation\\Blender\\blender.exe'}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def config_file_exist(name):
    return os.path.isfile(name)

def config_get_default():
    '''
    Read and return default values
    '''
    config = configparser.ConfigParser()

    if not config_file_exist('config.ini'):
        generate_config_file()
    config.read('config.ini')
    return config['DEFAULT']['image_path'], config['DEFAULT']['blender_installation_path']

def save_to_file(file_path, data):
    '''
    Save to file
    Saves our resulting array as json in file.
    @Param file_path, path to outputfile
    @Param data, data to write to file
    '''
    with open(file_path+'.txt', 'w') as f:
        f.write(json.dumps(data))

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

def get_current_path():
    '''
    Get path to this programs path
    '''
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return dir_path

def find_program_path(name):
    return which(name)
