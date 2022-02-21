from . import IO
from . import execution
from . import const
from . import floorplan

"""
Stacking
This file contains functions for handling stacking file parsing and creating larger stacking.

FloorplanToBlender3d
Copyright (C) 2022 Daniel Westberg
"""

def parse_stacking_file(path):
    """
    Parse strictly formated stacking files.
    These are used to more easily place many floorplans in one scene.
    """
    array_of_commands = IO.readlines_file(path)

    world = []
    worlds = []

    print("Building stack from file "+path)

    for  index, line in enumerate(array_of_commands):
        args = line.split(" ")
        command = args[0]


        if command[0] in ["#","\n",""," "]:  # ignore commented lines
            continue
        
        try:
            args.remove("\n")
        except Exception:
            pass
        
        new_args = []
        for cmd in args:
            if cmd == "\"_\"":
                new_args.append("None")
            else:
                new_args.append(cmd)
        args = new_args


        if command == "SEPARATE":
            worlds.append(world)
            world = []

        
        argstring = ""
        for index,arg in enumerate(args[1:]):
            if index == len(args[1:])-1:
                argstring+= arg
            else:
                argstring += arg+","


        print(">Line",index,"Command:",command+"("+argstring+")")

        world.append(eval(command+"("+argstring+")"))

        print("OK")

        if line == array_of_commands[-1]:
            worlds.append(world)

    print(path + " DONE!")

    return worlds

def FILE(stacking_file_path):
    return parse_stacking_file(stacking_file_path)

def ADD(
    config=None,
    image_path=None,
    amount=1,
    mode="x",
    margin=[0,0,0],
    worldpositionoffset=[0,0,0],
    worldrotationoffset=[0,0,0],
    worldscale=[1,1,1],
    amount_per_level=None,
    radie=None,
    degree=None
): 
    """
    Add floorplan to configuration
    """
    conf = config
    if config is None:
        conf = const.IMAGE_DEFAULT_CONFIG_FILE_NAME

    floorplans = []
    for _ in range(amount):
        floorplans.append(floorplan.new_floorplan(conf))

    if image_path is not None: # replace all image paths
        new_floorplans = []
        for f in floorplans:
            tmp_f = f
            tmp_f.image_path = image_path
            new_floorplans.append(tmp_f)
        floorplans = new_floorplans

    dir = 1
    if mode[0] == "-":
        dir = -1
        mode = mode[1]

    if mode == "cylinder":
        return execution.multiple_cylinder(
            floorplans, amount_per_level, radie, degree, dir, margin, worldpositionoffset, worldrotationoffset, worldscale
        )
    else:
        return execution.multiple_axis(floorplans, mode, dir, margin, worldpositionoffset, worldrotationoffset, worldscale)
