from enum import Enum

"""
Const
This file contains contants to remove "magic" numbers and strings.

Use this file to customize all strings in program easily from one place.
Be careful changing these.

FloorplanToBlender3d
Copyright (C) 2022 Daniel Westberg
"""

# Main script
SUPPORTED_BLENDER_FORMATS = (
    ".obj",
    ".x3d",
    ".gltf",
    ".mtl",
    ".webm",
    ".blend",
    ".vrml",
    ".usd",
    ".udim",
    ".stl",
    ".svg",
    ".dxf",
    ".fbx",
    ".3ds",
)
BASE_FORMAT = ".blend"


class MODE(Enum):
    AXIS = 0
    CYLINDER = 1


# Paths to save folder
BASE_PATH = "Data/"
TARGET_PATH = "/Target/"
TARGET_NAME = "floorplan"
BLENDER_SCRIPT_PATH = "Blender/floorplan_to_3dObject_in_blender.py"

# Generators
WALL_GROUND = 0
WALL_HEIGHT = 1
PIXEL_TO_3D_SCALE = 100

# Paths to models
DOOR_MODEL = "Images/Models/Doors/door.png"  # TODO: make dynamic folder solution, to add more doors!
DOOR_WIDTH = 5

# Data creation
ROOM_FLOOR_DISTANCE = 0.001  # place room slightly above floor
WINDOW_MIN_MAX_GAP = [0.25, 0.75]  # change window gap size

# Detection
# These are mostly calibrated variables that might need some changes.
# these might be intresting to temper with, but might give unexpected results!

# Box detection
PRECISE_BOXES_ACCURACY = 0.001
REMOVE_PRECISE_BOXES_ACCURACY = 0.001
OUTER_CONTOURS_TRESHOLD = [230, 255]
PRECISE_HARRIS_KERNEL_SIZE = (1, 1)
PRECISE_HARRIS_BLOCK_SIZE = 2
PRECISE_HARRIS_KSIZE = 3
PRECISE_HARRIS_K = 0.04
PRECISE_ERODE_ITERATIONS = 10

# Room detection
FIND_ROOMS_NOISE_REMOVAL_THRESHOLD = 50
FIND_ROOMS_CORNERS_THRESHOLD = 0.01
FIND_ROOMS_CLOSING_MAX_LENGTH = 130
FIND_ROOMS_GAP_IN_WALL_MIN_THRESHOLD = 5000

# Generic filters
WALL_FILTER_TRESHOLD = [0, 255]
WALL_FILTER_KERNEL_SIZE = (3, 3)
WALL_FILTER_MORPHOLOGY_ITERATIONS = 2
WALL_FILTER_DILATE_ITERATIONS = 3
WALL_FILTER_DISTANCE = 5
WALL_FILTER_DISTANCE_THRESHOLD = [0.5, 0.2]
WALL_FILTER_MAX_VALUE = 255
WALL_FILTER_THRESHOLD_TECHNIQUE = 0

# Windows and doors
WINDOWS_AND_DOORS_FEATURE_N = 10000000
WINDOWS_AND_DOORS_MAX_CORNERS = 4
WINDOWS_AND_DOORS_FEATURE_TRACK_MAX_CORNERS = 3
WINDOWS_AND_DOORS_FEATURE_TRACK_QUALITY = 0.01
WINDOWS_AND_DOORS_FEATURE_TRACK_MIN_DIST = 20

DOOR_ANGLE_HIT_STEP = 30  # Preferably evenly dividable with 360

WINDOWS_COLORED_PIXELS_THRESHOLD = [0.001, 0.00459]
WINDOWS_RESCALE_TO_FIT = 1.05

DETAILS_NOISE_REMOVAL_THRESHOLD = 50
DETAILS_CORNERS_THRESHOLD = 0.01
DETAILS_CLOSING_MAX_LENGTH = 130
DETAILS_GAP_IN_WALL_THRESHOLD = [10, 5000]

# Imageing
IMAGE_H = 10
IMAGE_HCOLOR = 10
IMAGE_TEMPLATE_SIZE = 7
IMAGE_SEARCH_SIZE = 21

# DEBUG modes # TODO: implement these!
DEBUG_DOOR = False
DEBUG_WINDOW = False
DEBUG_FLOOR = False
DEBUG_ROOM = False
DEBUG_WALL = False

# CONFIG
SYSTEM_CONFIG_FILE_NAME = "./Configs/system.ini"
IMAGE_DEFAULT_CONFIG_FILE_NAME = "./Configs/default.ini"

# CONFIG field/key names
# These values are used as backup incase config.ini can't be found.
# "STR" indicates that these are keys
STR_CALIBRATION_IMAGE_PATH = "calibration_image_path"
STR_WALL_SIZE_CALIBRATION = "wall_size_calibration"
STR_DEFAULT_SIZE_CALIBRATION = "default_calibration_image"
STR_IMAGE_PATH = "image_path"
STR_ORIGIN_PATH = "origin_path"
STR_SHAPE = "shape"
STR_OUT_FORMAT = "out_format"
STR_OVERWRITE_DATA = "overwrite_data"
STR_BLENDER_INSTALL_PATH = "blender_installation_path"
STR_FILE_STRUCTURE = "file_structure"
STR_MODE = "mode"
STR_DATA_PATH = "data_path"
STR_ROTATION = "rotation"
STR_POSITION = "position"

TRANSFORM_PATH = "/transform.txt"

STR_FLOORS = "floors"
STR_ROOMS = "rooms"
STR_WALLS = "walls"
STR_DOORS = "doors"
STR_WINDOWS = "windows"

STR_REMOVE_NOISE = "remove_noise"
STR_RESCALE_IMAGE = "rescale_image"

# CONFIG category names
SETTINGS = "EXTRA_SETTINGS"
DEFAULT = "DEFAULT_VALUES"
WALL_CALIBRATION = "WALL_CALIBRATION"
FEATURES = "FEATURES"

# CONFIG values
# These values will be set in config file if config.ini is removed!
DEFAULT_CALIBRATION_IMAGE_PATH = "Images/Calibrations/wallcalibration.png"
DEFAULT_IMAGE_PATH = "Images/Examples/example.png"
DEFAULT_OUT_FORMAT = ".blend"
DEFAULT_OVERWRITE_DATA = "False"
MAC_DEFAULT_BLENDER_INSTALL_PATH = "/Applications/Blender.app/Contents/MacOS/Blender"
LINUX_DEFAULT_BLENDER_INSTALL_PATH = "/usr/local/blender/blender"
WIN_DEFAULT_BLENDER_INSTALL_PATH = (
    "C:\\Program Files\\Blender Foundation\\Blender 2.90\\blender.exe"
)
DEFAULT_MODE = "HVSTACK"
DEFAULT_FEATURES = True
DEFAULT_REMOVE_NOISE = True
DEFAULT_RESCALE_IMAGE = True
DEFAULT_WALL_SIZE_CALIBRATION = 0

# DATA save files names
FLOOR_VERTS = "floor_verts"
FLOOR_FACES = "floor_faces"
ROOM_VERTS = "room_verts"
ROOM_FACES = "room_faces"
WALL_VERTICAL_VERTS = "wall_vertical_verts"
WALL_VERTICAL_FACES = "wall_vertical_faces"
WALL_HORIZONTAL_VERTS = "wall_horizontal_verts"
WALL_HORIZONTAL_FACES = "wall_horizontal_faces"
WINDOW_VERTICAL_VERTS = "window_vertical_verts"
WINDOW_VERTICAL_FACES = "window_vertical_faces"
WINDOW_HORIZONTAL_VERTS = "window_horizontal_verts"
WINDOW_HORIZONTAL_FACES = "window_horizontal_faces"
DOOR_VERTICAL_VERTS = "door_vertical_verts"
DOOR_VERTICAL_FACES = "door_vertical_faces"
DOOR_HORIZONTAL_VERTS = "door_horizontal_verts"
DOOR_HORIZONTAL_FACES = "door_horizontal_faces"
SAVE_DATA_FORMAT = ".txt"
