
"""
Const
This file contains contants to remove "magic" numbers and strings.

FloorplanToBlender3d
Copyright (C) 2021 Daniel Westberg
"""

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


# TODO: move more variables here!
# TODO: fix debug modes here!