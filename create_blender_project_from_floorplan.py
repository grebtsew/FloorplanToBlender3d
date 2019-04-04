from subprocess import check_output
from FloorplanToBlenderLib import * # floorplan to blender lib
import os
from pyfiglet import Figlet
f = Figlet(font='slant')
print (f.renderText('Floorplan to Blender3d'))

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
    var = input("Please enter your floorplan image paths seperated by space [default = " + image_path+"]: ")
    if var:
        image_paths  = var.split()
    var = input("Please enter your blender installation path [default = " +blender_install_path+"]: ")
    if var:
        blender_install_path = var

    print("")
    var = input("This program is about to run and create blender3d project, continue?  [default = " + "OK"+"]: ")
    if var:
        print("Program stopped.")
        exit(0)

    print("")
    print("Generate datafiles in folder: Data")
    print("")
    print("Clean datafiles")
    print("")

    IO.clean_data_folder("Data/")

    # Ask how floorplans shall be structured

    # Generate data files
    data_paths = list()
    fshape = None
    # for each input image path!
    for image_path in image_paths:
        # Calculate positions and rotations here!

        # Generate all data for imagepath
        fpath, fshape = generate.generate_all_files(image_path, True)

        # add path to send to blender
        data_paths.append(fpath)

    print("")
    print("Creates blender project")
    print("")

    # Create blender project
    check_output([blender_install_path,
     "--background",
     "--python",
     blender_script_path,
     program_path # Send this as parameter to script
     ] +  data_paths)

    print("Project created at: " + program_path + "\\floorplan.blender")
    print("")
    print("Done, Have a nice day!")
