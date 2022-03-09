from . import IO
from . import execution
from . import const
from . import floorplan
from . import transform

import numpy as np

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

    print("Building stack from file " + path)

    for index, line in enumerate(array_of_commands):
        args = line.split(" ")
        command = args[0]

        if command[0] in ["#", "\n", "", " "]:  # ignore commented lines
            continue

        try:
            args.remove("\n")
        except Exception:
            pass

        new_args = []
        for cmd in args:
            if cmd == '"_"':
                new_args.append("None")
            else:
                new_args.append(cmd)
        args = new_args

        argstring = ""
        for index, arg in enumerate(args[1:]):
            if index == len(args[1:]) - 1:
                argstring += arg
            else:
                argstring += arg + ","

        print(">Line", index, "Command:", command + "(" + argstring + ")")

        if command == "SEPARATE":
            worlds.append(world)
            world = []
        elif command == "CLEAR":
            eval(command + "(" + argstring + ")")
        else:
            world.extend(eval(command + "(" + argstring + ")"))

    worlds.extend(world)
    return worlds


def CLEAR():
    IO.clean_data_folder(const.BASE_PATH)


def SEPARATE():
    pass


def FILE(stacking_file_path):
    return parse_stacking_file(stacking_file_path)


def ADD(
    config=None,
    image_path=None,
    amount=1,
    mode="x",
    margin=np.array([0, 0, 0]),
    worldpositionoffset=np.array([0, 0, 0]),
    worldrotationoffset=np.array([0, 0, 0]),
    worldscale=np.array([1, 1, 1]),
    amount_per_level=None,
    radie=None,
    degree=None,
):
    """
    Add floorplan to configuration
    """
    conf = config
    if config is None:
        conf = const.IMAGE_DEFAULT_CONFIG_FILE_NAME

    if amount is None:
        amount = 1

    floorplans = []
    for _ in range(amount):
        floorplans.append(floorplan.new_floorplan(conf))

    if image_path is not None:  # replace all image paths
        new_floorplans = []
        for f in floorplans:
            tmp_f = f
            tmp_f.image_path = image_path
            new_floorplans.append(tmp_f)
        floorplans = new_floorplans

    dir = 1
    if mode is None:
        mode = "x"
    if mode[0] == "-":
        dir = -1
        mode = mode[1]

    if mode == "cylinder":
        return execution.multiple_cylinder(
            floorplans,
            amount_per_level,
            radie,
            degree,
            world_direction=dir,
            world_position=transform.list_to_nparray(
                worldpositionoffset, np.array([0, 0, 0])
            ),
            world_rotation=transform.list_to_nparray(
                worldrotationoffset, np.array([0, 0, 0])
            ),
            world_scale=transform.list_to_nparray(worldscale),
            margin=transform.list_to_nparray(margin, np.array([0, 0, 0])),
        )
    else:
        return execution.multiple_axis(
            floorplans,
            mode,
            dir,
            transform.list_to_nparray(margin, np.array([0, 0, 0])),
            transform.list_to_nparray(worldpositionoffset, np.array([0, 0, 0])),
            transform.list_to_nparray(worldrotationoffset, np.array([0, 0, 0])),
            transform.list_to_nparray(worldscale),
        )
