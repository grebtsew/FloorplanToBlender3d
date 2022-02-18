from subprocess import check_output
from FloorplanToBlenderLib import (
    IO,
    config,
    const,
    execution,
    dialog,
    floorplan,
    stacking,
)  # floorplan to blender lib
import os

# TODO:s need fixing before next merge with main -
# - floorplan class
# - floorplan config
# - margin
# - add floor / roof
# - test dockerfile
# - secure window and door detections, as selectable settings
# - go through all TODO:s and solve easy to fix ones, create issues for the rest
# - create issue for multi model doors
# - create issue for use logging and f''
# - update demos
# - update readme
# - create CI/CD action
# - update license dates

"""
Create Blender Project from floorplan
This file contains a simple example implementation of creations of 3d models from
floorplans. You will need blender and an image of a floorplan to make this work.

FloorplanToBlender3d
Copyright (C) 2021 Daniel Westberg
"""
def create_blender_project(data_paths):
    if not os.path.exists("." + target_folder):
        os.makedirs("." + target_folder)

    target_base = target_folder + const.TARGET_NAME
    target_path = target_base + const.BASE_FORMAT
    target_path = (
        IO.get_next_target_base_name(target_base, target_path) + const.BASE_FORMAT
    )

    # Create blender project
    check_output(
        [
            blender_install_path,
            "-noaudio",  # this is a dockerfile ubuntu hax fix
            "--background",
            "--python",
            blender_script_path,
            program_path,  # Send this as parameter to script
            target_path,
        ]
        + data_paths
    )

    # Transform .blend project to another format!
    if outformat != ".blend":
        check_output(
            [
                blender_install_path,
                "-noaudio",  # this is a dockerfile ubuntu hax fix
                "--background",
                "--python",
                "./Blender/blender_export_any.py",
                "." + target_path,
                outformat,
                target_base + outformat,
            ]
        )
        print("Object created at:" + program_path + target_base + outformat)

    print("Project created at: " + program_path + target_path)


if __name__ == "__main__":
    """
    Do not change variables in this file but rather in ./config.ini or ./FloorplanToBlenderLib/const.py
    """
    dialog.figlet()

    image_path = ""
    blender_install_path = ""

    data_folder = const.BASE_PATH

    target_folder = const.TARGET_PATH

    blender_install_path = config.get_default_blender_installation_path() # TODO: update this

    # Set other paths (don't need to change these)
    floorplans = []
    program_path = os.path.dirname(os.path.realpath(__file__))
    blender_script_path = const.BLENDER_SCRIPT_PATH

    dialog.init()

    image_paths = []

    var = input(
        "Do you want to build from file or manually ? [default = manually]: "
    )
    if var:
        stacking_def_path = "./Stacking/example.txt"
        var = input(
        f"Enter path to Stacking file : [default = {stacking_def_path}]: "
        )
        if var:    
            stacking_def_path = var
        data_paths = stacking.parse_stacking_file(stacking_def_path)
    else:
        
        # Detect where/if blender is installed on pc
        auto_blender_install_path = IO.blender_installed()

        if auto_blender_install_path is not None:
            blender_install_path = auto_blender_install_path

        var = input(
            "Please enter your blender installation path [default = "
            + blender_install_path
            + "]: "
        )
        if var:
            blender_install_path = var

        config_path = "./Configs/default.ini"
        var = input(
            "Use default config or import from file [default = "
            + config_path
            + "]: "
        )

        if var:
            # TODO: space separated list off configs!
            config_path = var
            
            floorplans.append(floorplan.new_floorplan(c) for c in config_path.split(" "))
            #floorplans = [floorplan.new_floorplan(config)]
        else:
            image_path = config.get_default_image_path() # TODO: update this
            var = input(
            "Please enter your floorplan image paths seperated by space [default = "
            + image_path
            + "]: "
            )
            if var:
                image_paths = var.split()
            else:
                #TODO: get default image_path, mode
                image_paths = image_path.split()

            outformat = config.get(const.IMAGE_DEFAULT_CONFIG_FILE_NAME, "IMAGE")[const.STR_OUT_FORMAT]
            var = input(
                "Please enter your preferred blender supported output format [default = "
                + outformat
                + "]: "
            )
            if var in const.SUPPORTED_BLENDER_FORMATS:
                outformat = var

            # Advanced Settings
            settings = config.get(const.IMAGE_DEFAULT_CONFIG_FILE_NAME)  # TODO: fix and update config file

            var = input("Do you want to change advanced settings [default = No]: ")
            if var == "Yes" or var == "yes":
                var = input(
                    "Use noise removal [default = " + settings[const.SETTINGS][const.STR_REMOVE_NOISE] + "]: "
                )
                if var == "Yes" or var == "yes":
                    settings[const.SETTINGS][const.STR_REMOVE_NOISE] = "True"
                elif var == "No" or var == "no":
                    settings[const.SETTINGS][const.STR_REMOVE_NOISE] = "False"

                var = input(
                    "Use auto image resize [default = " + const.STR_RESCALE_IMAGE + "]: "
                )
                if var == "Yes" or var == "yes":
                    settings[const.SETTINGS][const.STR_RESCALE_IMAGE] = "True"
                elif var == "No" or var == "no":
                    settings[const.SETTINGS][const.STR_RESCALE_IMAGE] = "False"
            
            # Save new settings to config file
            # Delete config file to reset it to default
            config.update(const.IMAGE_DEFAULT_CONFIG_FILE_NAME, const.SETTINGS, settings)

            floorplans = [floorplan.new_floorplan(config_path) for _ in image_paths] # Load all configs into memory
           
        print("")
        var = input(
            "This program is about to run and create blender3d project, continue? : "
        )
        if var:
            print("Program stopped.")
            exit(0)

        print("")
        print("Generate datafiles in folder: Data")
        print("")
        print("Clean datafiles")

        print("")
        # TODO: should be part of system config
        var = input("Clear all cached data before run: [default = yes] : ")

        if not var or var.lower() == "yes" or var.lower() == "y":
            IO.clean_data_folder(data_folder)

        # Generate data files
        data_paths = list()
        fshape = None

        # Ask how floorplans shall be structured
        if len(image_paths) > 1:
            print("There are currently " + str(len(image_paths)) + " floorplans to create.")

            var = input(
                "Which mode do you want to  use for multi floorplan stacking [AXIS,CYLINDER,FILE,HVSTACK,SEPARATED] [default = "
                + mode
                + " ] ?"
            )
            if var:
                mode = var

            if mode == "HVSTACK":
                var = input("Do you want to build horizontal? [Yes] : ")
                if var:
                    data_paths = execution.multiple_simple(image_paths, False)
                else:
                    data_paths = execution.multiple_simple(image_paths, True)
            elif mode == "AXIS":
                
                axis = "-z"
                var = input(
                    f"Which axis do you want to stack on [X,-X,Y,-Y,Z,-Z] [default = {axis}] : "
                )
                if var:
                    axis = var
                dir = 1
                if axis[0] == "-":
                    dir = -1
                    axis = axis[1]
                data_paths = execution.multiple_axis(image_paths, axis, dir)
            elif mode == "CYLINDER":
                degrees = 360
                radie = 10
                amount = 4
                var = input(f"How many degrees [0-360] [default = {degrees}] : ")
                if var:
                    degrees = var
                var = input(f"How many floorplans per level [default = {amount}] : ")
                if var:
                    amount = var
                var = input(f"Radie [default = {radie}] : ")
                if var:
                    radie = var
                data_paths = execution.multiple_cylinder(
                    image_paths, amount, radie, degrees, dir
                )
            elif mode == "SEPARATED":
                data_paths = [[execution.simple_single(image)] for image in image_paths]
        else:
            data_paths = [execution.simple_single(image_paths[0])]

    print("")
    print("Creates blender project")
    print("")

    if mode == "SEPARATED":
        for data_path in data_paths:
            create_blender_project(data_path)
    else: 
        create_blender_project(data_paths)

    print("")
    print("Done, Have a nice day!")

    dialog.end_copyright()
