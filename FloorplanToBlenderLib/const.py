
"""
Const
This file contains contants to remove "magic" numbers and strings.

Use this file to customize all strings in program.

FloorplanToBlender3d
Copyright (C) 2021 Daniel Westberg
"""

# Main script
SUPPORTED_BLENDER_FORMATS = ('.obj','.x3d', '.gltf','.mtl','.webm','.blend','.vrml','.usd','.udim','.stl','.svg','.dxf','.fbx','.3ds')
BASE_FORMAT = ".blend"

# Paths to save folder
BASE_PATH = "Data/"

# Generators
WALL_HEIGHT = 1
PIXEL_TO_3D_SCALE = 100

# Paths to models
DOOR_MODEL = "Images/Models/Doors/door.png" # TODO: make dynamic folder solution, to add more doors!
DOOR_WIDTH = 5

# DEBUG modes

DEBUG_DOOR = False
DEBUG_WINDOW = False
DEBUG_FLOOR = False
DEBUG_ROOM = False
DEBUG_WALL = False

# CONFIG
CONFIG_FILE_NAME ='config.ini'

# CONFIG field names
STR_WALL_CALIBRATION = "WALL_CALIBRATION"
STR_CALIBRATION_IMAGE_PATH = "calibration_image_path"
STR_WALL_SIZE_CALIBRATION = "wall_size_calibration"

# CONFIG category names
SETTINGS = "SETTINGS"
DEFAULT = "DEFAULT"
WALL_CALIBRATION = "WALL_CALIBRATION"
FEATURES = "FEATURES"

# CONFIG values



# TODO: move more variables here!
# TODO: fix debug modes here!