from subprocess import check_output
from FloorplanToBlenderLib import * # floorplan to blender lib
import os


'''
Start here
'''
if __name__ == "__main__":

    # Set required default paths
    image_path = "" # path the your image
    blender_install_path = "" # path to blender installation folder

    image_path, blender_install_path = IO.config_get_default()

    # Set other paths (don't need to change these)
    program_path = os.path.dirname(os.path.realpath(__file__))
    blender_script_path = "Blender/floorplan_to_3dObject_in_blender.py"

    # Create some gui
    print( "----- CREATE BLENDER PROJECT FROM FLOORPLAN WITH DIALOG -----" )
    print("Welcome to this program. Please answer the questions below to progress.")
    print("Remember that you can change default paths in the config file.")
    print("")

    # Some input
    var = input("Please enter your floorplan image path [default = " + image_path+"]: ")
    if var:
        image_path = var
    var = input("Please enter your blender installation path [default = " +blender_install_path+"]: ")
    if var:
        blender_install_path = var

    print("")
    print("Generate datafiles in folder: Data")
    print("")

    # Generate data files
    generate.generate_all_files(image_path, True)

    print("")
    print("Creates blender project")
    print("")

    # Create blender project
    check_output([blender_install_path,
     "--background",
     "--python",
     blender_script_path,
     program_path # Send this as parameter to script
     ])

    print("Project created at: " + program_path + "\\floorplan.blender")
    print("")
    print("Done, Have a nice day!")
