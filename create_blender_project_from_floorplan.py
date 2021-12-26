from subprocess import check_output
from FloorplanToBlenderLib import (
    IO,
    config,
    const,
    execution,
    dialog,
)  # floorplan to blender lib
import os

# TODO: remove objects outside of detected floor!
# TODO:s need fixing before next merge with main -
# - finish floorplan stacking atleast 100+
# - test dockerfile
# - secure window and door detections, as selectable settings
# - go through all TODO:s and solve easy to fix ones, create issues for the rest
# - multi model doors
# - updated demos
# - update readme
# - create CI/CD action

"""
Create Blender Project from floorplan
This file contains a simple example implementation of creations of 3d models from
floorplans. You will need blender and an image of a floorplan to make this work.

FloorplanToBlender3d
Copyright (C) 2021 Daniel Westberg
"""
if __name__ == "__main__":
    """
    Do not change variables in this file but rather in ./config.ini or ./FloorplanToBlenderLib/const.py
    """
    dialog.figlet()

    image_path = ""
    blender_install_path = ""

    data_folder = const.BASE_PATH

    target_folder = const.TARGET_PATH

    image_path, blender_install_path, file_structure, mode = config.get_default()

    # Set other paths (don't need to change these)
    program_path = os.path.dirname(os.path.realpath(__file__))
    blender_script_path = const.BLENDER_SCRIPT_PATH

    # Create some gui
    dialog.init()

    # Some input
    image_paths = []
    var = input(
        "Please enter your floorplan image paths seperated by space [default = "
        + image_path
        + "]: "
    )
    if var:
        image_paths = var.split()
    else:
        image_paths = image_path.split()

    # Detect where/if blender is installed on pc
    auto_blender_install_path =IO.blender_installed()

    if auto_blender_install_path is not None:
        blender_install_path = auto_blender_install_path

    var = input(
        "Please enter your blender installation path [default = "
        + blender_install_path
        + "]: "
    )
    if var:
        blender_install_path = var

    outformat = config.get(const.DEFAULT)[const.STR_OUT_FORMAT]
    var = input(
        "Please enter your preferred blender supported output format [default = "
        + outformat
        + "]: "
    )
    if var in const.SUPPORTED_BLENDER_FORMATS:
        outformat = var

    # Advanced Settings
    settings = config.get(const.SETTINGS)  # TODO: fix and update config file

    var = input("Do you want to change advanced settings [default = No]: ")
    if var == "Yes" or var == "yes":
        var = input(
            "Use noise removal [default = " + settings[const.STR_REMOVE_NOISE] + "]: "
        )
        if var == "Yes" or var == "yes":
            settings[const.STR_REMOVE_NOISE] = "True"
        elif var == "No" or var == "no":
            settings[const.STR_REMOVE_NOISE] = "False"

        var = input(
            "Use auto image resize [default = " + const.STR_RESCALE_IMAGE + "]: "
        )
        if var == "Yes" or var == "yes":
            settings[const.STR_RESCALE_IMAGE] = "True"
        elif var == "No" or var == "no":
            settings[const.STR_RESCALE_IMAGE] = "False"

    print("")
    var = input(
        "This program is about to run and create blender3d project, continue? : "
    )
    if var:
        print("Program stopped.")
        exit(0)

    # Save new settings to config file
    # Delete config file to reset it to default
    config.update(const.SETTINGS, settings)

    print("")
    print("Generate datafiles in folder: Data")
    print("")
    print("Clean datafiles")

    IO.clean_data_folder(data_folder)

    # Generate data files
    data_paths = list()
    fshape = None

    # Ask how floorplans shall be structured
    if len(image_paths) > 1:  # TODO:, default multi execution is [ "+mode +" ]")
        print("There are currently " + str(len(image_paths)) + " floorplans to create.")

        var = input(
            "Do you want to build horizontal? [Yes] : "
        )  # TODO: vertical + matrix
        if var:
            data_paths = execution.multiple_simple(image_paths, False)
        else:
            data_paths = execution.multiple_simple(image_paths, True)
    else:
        data_paths = [execution.simple_single(image_paths[0])]

    print("")
    print("Creates blender project")
    print("")

    if not os.path.exists("."+target_folder):
        os.makedirs("."+target_folder)

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
    print("")
    print("Done, Have a nice day!")

    dialog.end_copyright()
