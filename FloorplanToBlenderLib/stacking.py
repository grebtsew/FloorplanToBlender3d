from . import IO
from . import execution

"""
Stacking
This file contains functions for handling stacking file parsing and creating larger stacking.

FloorplanToBlender3d
Copyright (C) 2021 Daniel Westberg
"""

def parse_stacking_file(path):
    """
    Parse strictly formated stacking files.
    These are used to more easily place many floorplans in one scene.
    """
    array_of_commands = IO.readlines_file(path)
    
    world = []

    for line in array_of_commands:
        args = line.split(" ")
        command = args[0]

        if command[0] == "#": # ignore commented lines
            continue

        world.append(eval(command(args[1:])))
    
    return world

def ADD(image_path, amount, axis, pos, rot, sca, amount_per_level=None, radie=None, degree=None):
    """
    Add floorplan to configuration
    """
    image_paths = [image_path for i in range(amount)]
    dir = 1

    if axis[0] == "-":
        dir = -1
        axis = axis[1]
    
    if axis == "cylinder":
        return execution.multiple_cylinder(image_paths, amount_per_level, radie, degree, dir, pos, rot, sca )
    else:
        return execution.multiple_axis(image_paths,axis,dir, pos, rot, sca )